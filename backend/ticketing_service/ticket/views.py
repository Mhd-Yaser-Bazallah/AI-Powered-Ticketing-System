    
import logging
from injector import inject 
from rest_framework.views import APIView
from sqlalchemy import Transaction
from notification.repositories import NotificationRepository
from notification.services import NotificationService
from team.models import Team
from team.repositories import TeamRepository
from .services import TicketService
from .repositories import TicketRepository
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from users_management.permissions import IsClient, IsSupportTeamManager, IsSupportTeamMember, IsUser, IsSupportStaff
from .serializers import TicketSerializer, TicketCreateUpdateSerializer, SolveTicketSerializer
from users_management.models import CustomUser
from ticket_log.services import TicketLogService    
from ticket_log.repositories import ticketLogRepository    
from Issue_management.Issue   import Issue
from workflow_management.repositories import WorkflowRepository
from workflow_management.models import WorkflowStep
from django.db import transaction
from django.utils import timezone
from company.models import Company
from ticket.services_analyze_client import AnalyzeServiceClient, AnalyzeServiceError
from ticket.rag_client import build_ticket_payload, publish_ticket_created

logger = logging.getLogger(__name__)
class BaseTicketView(APIView):
        @inject
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.TicketService = TicketService(TicketRepository(),TeamRepository())
            self.ticketLogRepository =ticketLogRepository
            self.workflow_repo = WorkflowRepository()
            self.notification_service = NotificationService(NotificationRepository())


class CustomPagination(PageNumberPagination):
        page_size = 10  
        page_size_query_param = 'page_size'
        max_page_size = 100

        def get_paginated_response(self, data):
            
            total_pages = (self.page.paginator.count + self.page_size - 1) // self.page_size
            
            return Response({
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'total_pages': total_pages,                        
                'results': data
            })


class ListTicketView(BaseTicketView):
 
  
        pagination_class = CustomPagination

 
        def get(self, request):
 
            ticket = self.TicketService.list_ticket()
            paginator = self.pagination_class()
            paginated_ticket = paginator.paginate_queryset(ticket, request)
            return paginator.get_paginated_response(TicketSerializer(paginated_ticket, many=True).data)

class CreateTicketView(BaseTicketView):

    def post(self, request):
        serializer = TicketCreateUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            validated_data = serializer.validated_data
            description = validated_data["description"]
            title = validated_data["title"]
            company_id = validated_data["company"]
            client_id = validated_data["client"]
                               
            analyze_client = AnalyzeServiceClient()
            try:
                analysis = analyze_client.analyze(description, company_id)
                category = analysis["category"]
                priority = analysis["priority"]
                team_assignment = analysis.get("team_assignment") or {}
                if not isinstance(team_assignment, dict):
                    team_assignment = {}
            except AnalyzeServiceError as exc:
                logger.warning("Analyze service failed, using defaults: %s", exc)
                category = "back"
                priority = "low"
                team_assignment = {"need_admin": True}
                      
            workflow_repo = WorkflowRepository()
            company_obj = Company.objects.get(id=company_id)
            workflow = workflow_repo.get_workflow_by_company(company_obj) or workflow_repo.get_global_workflow()
            if not workflow:
                return Response({"error": "No workflow defined."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            steps = workflow_repo.get_steps_for_workflow(workflow)
            if not steps:
                return Response({"error": "Workflow has no steps."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            first_status = steps[0].name          
            with transaction.atomic():
                                  
                ticket = self.TicketService.create_ticket(
                    description=description,
                    title=title,
                    company_id=company_id,
                    client_id=client_id,
                    priority=priority,
                    category=category,
                    status=first_status
                ) 
                                           
                assigned_team = None
                if ticket.company and ticket.company.auto_assign:
                    need_admin = bool(team_assignment.get("need_admin"))
                    ticket.need_admin = need_admin
                    ticket.bert_category = team_assignment.get("bert_category")
                    ticket.bert_confidence = team_assignment.get("bert_confidence")
                    ticket.similarity_score = team_assignment.get("similarity_score")
                    if not need_admin:
                        team_id = team_assignment.get("assigned_team_id")
                        if team_id:
                            assigned_team = Team.objects.filter(id=team_id, company_id=company_id).first()
                        if assigned_team:
                            self.TicketService.assign_ticket_to_team(ticket.id, assigned_team.id)
                        else:
                               
                            ticket.need_admin = True
                    else:
                        ticket.need_admin = True

                    ticket.save(update_fields=[
                        "need_admin", "bert_category", "bert_confidence", "similarity_score"
                    ])

                            
                self.ticketLogRepository.create_ticketLog(
                    self,
                    ticket=ticket.id,
                    user=ticket.client_id,                                        
                    action="Ticket Creation",
                    previous_status="Null",
                    new_status=first_status,
                    comments="ticket created successfully",
                    company=ticket.company_id
                )

                                  
                self.notification_service.notify_user(
                    ticket.client, ticket, "Ticket created successfully", ticket.company
                )

                if assigned_team and not ticket.need_admin:
                    self.notification_service.notify_team(
                        assigned_team,
                        ticket,
                        f"Ticket '{ticket.title}' has been assigned automatically to your team.",
                        ticket.company
                    )
                elif ticket.need_admin and ticket.company and ticket.company.auto_assign:
                                              
                                                                 
                    pass

                event_payload = build_ticket_payload(
                    ticket,
                    assigned_team_id=(assigned_team.id if assigned_team else None),
                )
                transaction.on_commit(
                    lambda: publish_ticket_created(event_payload)
                )

            return Response(TicketSerializer(ticket).data, status=status.HTTP_201_CREATED)

        except Company.DoesNotExist:
            return Response({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClientTicketView(BaseTicketView):
        
        def get(self, request,client_id):
   
            ticket = self.TicketService.client_tickets(client_id)
            serialized_data = TicketSerializer(ticket, many=True).data
            response_data = {
                "results": serialized_data
            }
         
            return Response(response_data, status=status.HTTP_200_OK)


class CompanyTicketView(BaseTicketView):
        permission_classes = [IsUser] 

 
        def get(self, request,company_id):
 
            ticket = self.TicketService.company_tickets(company_id)
            
            serialized_data = TicketSerializer(ticket, many=True).data
            response_data = {
                "results": serialized_data
            }
         
            return Response(response_data, status=status.HTTP_200_OK)
         

class AssignTicketToTeamView(BaseTicketView):
                                                     

        def post(self, request, ticket_id):
            team_id = request.data.get("team_id")
            if not ticket_id:
                return Response({"error": "ticket_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            try: 
                ticket = self.TicketService.TicketRepository.get_ticket_by_id(ticket_id)
                current_state = Issue(ticket.status) 
                next_state = current_state.change_state()
                self.TicketService.update_ticket(ticket_id,validated_data={"status": next_state})
 
                user_instance = Team.objects.get(id=team_id)                             
                company_instance = ticket.company                           
                 
                assignment = self.TicketService.assign_ticket_to_team(ticket_id, team_id)
                if assignment:
                                                  
                            ticket_id = ticket.id
                            user=ticket.client.id
                            action="Ticket Assigen To Team"
                            previous_status= "Open"
                            new_status = "Assigen To Team"
                            comments= "ticket Assigen To Team successfully"
                            company = ticket.company.id
                                                                                                                     
                            self.ticketLogRepository.create_ticketLog(self,ticket_id,user,action,previous_status,new_status,comments,company) 
                            
                                                                                                                                        

                self.notification_service.notify_team(user_instance, ticket, f"Ticket:{ticket_id} has been assigned to your team", company_instance)
                return Response(
                    {
                        "message": f"Ticket {assignment.Ticket.id} assigned to team {assignment.Team.category} successfully.",
                        "new_status": ticket.status,
                    },
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST) 

            
class  TicketToInProgressView(BaseTicketView):
                                                    

        def post(self, request, ticket_id): 
            if not ticket_id:
                return Response({"error": "ticket_id is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                 
                ticket = self.TicketService.TicketRepository.get_ticket_by_id(ticket_id)
                current_state = Issue(ticket.status) 
                next_state = current_state.change_state()
                self.TicketService.update_ticket(ticket_id,validated_data={"status": next_state})

                            
                ticket_id = ticket.id
                user=ticket.client.id
                action="Ticket changed status To in Progress"
                previous_status= "Assigen To Team"
                new_status = "in Progress"
                comments= "Ticket changed status To in Progress successfully"
                company = ticket.company.id
                self.ticketLogRepository.create_ticketLog(self,ticket_id,user,action,previous_status,new_status,comments,company) 
                user_instance = ticket.client                             
                company_instance = ticket.company                           
                self.notification_service.notify_user(user_instance, ticket, f"The ticket status has been changed to:{new_status}", company_instance)
                return Response(
                    {
                        "message": f"Ticket {ticket.id} changed status to In Progress successfully.",
                        "new_status": ticket.status,
                    },
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class  TicketToDoneView(BaseTicketView):
        permission_classes = [IsSupportTeamMember]

        def post(self, request, ticket_id): 
            if not ticket_id:
                return Response({"error": "ticket_id is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                                  
                ticket = self.TicketService.TicketRepository.get_ticket_by_id(ticket_id)
                current_state = Issue(ticket.status) 
                next_state = current_state.change_state()
                self.TicketService.update_ticket(ticket_id,validated_data={"status": next_state})

                ticket_id = ticket.id
                user=ticket.client.id
                action="Ticket changed status To Done"
                previous_status= "in Progress"
                new_status = "Done"
                comments= "Ticket changed status To  Done successfully"
                company = ticket.company.id
                self.ticketLogRepository.create_ticketLog(self,ticket_id,user,action,previous_status,new_status,comments,company)
                user_instance = ticket.client                             
                company_instance = ticket.company                           
                                                                                                                                                       
                self.notification_service.notify_user(user_instance, ticket, f"The ticket status has been changed to:{new_status}", company_instance)               
                return Response(
                    {
                        "message": f"Ticket {ticket.id} changed status to Done successfully.",
                        "new_status": ticket.status,
                    },
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AssignTicketToMeView(BaseTicketView):
        permission_classes = [IsSupportTeamMember]

        def post(self, request, ticket_id):
            user_id = request.data.get("user_id")
            if not ticket_id:
                return Response({"error": "ticket_id is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
              
                ticket = self.TicketService.TicketRepository.get_ticket_by_id(ticket_id)
                
                current_state = Issue(ticket.status) 
                next_state = current_state.change_state()
                self.TicketService.update_ticket(ticket_id,validated_data={"status": next_state})


               
                assignment = self.TicketService.assign_ticket_to_user(ticket_id, user_id)
                if assignment:
                    ticket_id = ticket.id
                    user=user_id
                    action="Ticket assign to user"
                    previous_status= "Ticket assign to team"
                    new_status = "assign to user"
                    comments= "Ticket assign to user  successfully"
                    company = ticket.company.id
                    self.ticketLogRepository.create_ticketLog(self,ticket_id,user,action,previous_status,new_status,comments,company)      
                    user_instance = ticket.client                             
                    company_instance = ticket.company                           
                                                                                                                                                       
                    self.notification_service.notify_user(user_instance, ticket, f"The ticket: {ticket_id} status has been changed to you", company_instance)
        
                return Response(
                    {
                        "message": f"Ticket {assignment.Ticket.id} assigned to user {assignment.user.username} successfully.",
                        "new_status": ticket.status,
                    },
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SolveTicketView(BaseTicketView):
        permission_classes = [IsSupportStaff]

        def post(self, request, ticket_id):
            serializer = SolveTicketSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            steps_payload = serializer.validated_data["steps"]
            comment = serializer.validated_data.get("comment") or "Human solution submitted"
            user_id = serializer.validated_data.get("user_id")

            try:
                ticket = self.TicketService.TicketRepository.get_ticket_by_id(ticket_id)
                if not ticket:
                    return Response({"error": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)

                workflow_repo = WorkflowRepository()
                workflow = workflow_repo.get_workflow_by_company(ticket.company) or workflow_repo.get_global_workflow()
                if not workflow:
                    return Response({"error": "No workflow defined."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                steps = workflow_repo.get_steps_for_workflow(workflow)
                if not steps:
                    return Response({"error": "Workflow has no steps."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                last_status = steps[-1].name
                previous_status = ticket.status

                with transaction.atomic():
                    ticket.human_solution_steps = steps_payload
                    ticket.human_solved_at = timezone.now()
                    if user_id:
                        ticket.human_solved_by = CustomUser.objects.filter(id=user_id).first()
                    if ticket.status != last_status:
                        ticket.status = last_status

                    update_fields = ["human_solution_steps", "human_solved_at", "human_solved_by"]
                    if ticket.status != previous_status:
                        update_fields.append("status")
                    ticket.save(update_fields=update_fields)

                    log_user_id = user_id or ticket.client_id
                    self.ticketLogRepository.create_ticketLog(
                        self,
                        ticket=ticket.id,
                        user=log_user_id,
                        action="Ticket Solved",
                        previous_status=previous_status,
                        new_status=last_status,
                        comments=comment,
                        company=ticket.company_id,
                    )

                    self.notification_service.notify_user(
                        ticket.client,
                        ticket,
                        "Ticket solved with human steps.",
                        ticket.company,
                    )

                return Response(TicketSerializer(ticket).data, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateTicketView(BaseTicketView):
                                         

        def put(self, request, ticket_id):
            serializer = TicketCreateUpdateSerializer(data=request.data,partial=True)
                           
            if serializer.is_valid():
                           
                updated_ticket = self.TicketService.update_ticket(ticket_id, serializer.validated_data)
                serialized_ticket =TicketSerializer(updated_ticket).data
                return Response(serialized_ticket, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteTicketView(BaseTicketView):
        permission_classes = [IsClient]

        def delete(self, request, ticket_id):
            self.TicketService.delete_ticket(ticket_id)
            return Response(status=status.HTTP_200_OK)        
        

class GetTicketAssignToMeView(BaseTicketView):

        def get(self, request , user_id): 
            ticket = self.TicketService.ticket_assign_to_user(user_id)

            serialized_data = TicketSerializer(ticket, many=True).data
 
            response_data = {
                "results": serialized_data
            }

            
 
            return Response(response_data, status=200)


class GetTicketAssignToTeamView(BaseTicketView):

        def get(self, request , team_id): 
            ticket = self.TicketService.ticket_assign_to_team(team_id)

            serialized_data = TicketSerializer(ticket, many=True).data
            response_data = {
                "results": serialized_data
            }
 
 
            return Response(response_data, status=200)


class AdvanceTicketStatusView(BaseTicketView):
    def post(self, request, ticket_id):
        try:
            ticket = self.TicketService.TicketRepository.get_ticket_by_id(ticket_id)
            if not ticket:
                return Response({"error": "Ticket not found."}, status=404)

            company = ticket.company
            workflow_repo = WorkflowRepository()
            workflow = workflow_repo.get_workflow_by_company(company)  

            if not workflow:
                return Response({"error": "No workflow found for the company."}, status=500)

            steps = workflow_repo.get_steps_for_workflow(workflow)
            current_step_index = next((i for i, step in enumerate(steps) if step.name == ticket.status), None)

            if current_step_index is None:
                return Response({"error": f"Current status '{ticket.status}' not found in workflow."}, status=400)

            if current_step_index + 1 >= len(steps):
                return Response({"message": "Ticket is already in the final status."}, status=400)

            next_status = steps[current_step_index + 1].name
            previous_status = ticket.status
            ticket.status = next_status
            ticket.save()

          
            user_id = request.data.get("user_id")
            if user_id:
                user = CustomUser.objects.filter(id=user_id).first()
                if user:
                    self.ticketLogRepository.create_ticketLog(
                        self,
                        ticket.id,
                        user.id,
                        "Status Update",
                        previous_status,
                        next_status,
                        f"Advanced from {previous_status} to {next_status}",
                        company.id,
                    )
                user_instance = ticket.client                             
                company_instance = ticket.company                           
                                                                                                                                                       
            self.notification_service.notify_user(user_instance , ticket, f"The ticket status has been changed to:{next_status}", company_instance)
            return Response({"message": "Status updated successfully", "new_status": next_status}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
