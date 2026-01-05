 
from injector import inject
from django.db import transaction
from company.models import Company
from .models import Ticket, Ticket_Team_Assignment, Ticket_User_Assignment  
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from users_management.models import Membership ,CustomUser 
from datetime import date
from team.models import Team
class TicketRepository: 
    @inject
     

     
    def create_ticket(self, client, company, title, description,priority,category,status) -> Ticket:
        ticket = Ticket.objects.create(
            client_id=client,
            company_id=company,
            title=title,
            description=description,
            priority=priority,
            category = category,
            status = status
             
        )
        ticket.save()
        return ticket

 
    def get_all_ticket(self) -> QuerySet:
        return Ticket.objects.all().order_by('created_at')
    
    def get_client_tickets(self,client_id) -> QuerySet:
        return Ticket.objects.filter(client_id=client_id).order_by('created_at')
    
    def get_company_tickets(self,company_id) -> QuerySet:
        return Ticket.objects.filter(company_id=company_id).order_by('created_at')
    
    def get_ticket_by_id(self, ticket_id: int) -> Ticket:
    
        return Ticket.objects.get(id=ticket_id)
         
    
    def assign_ticket_to_team(self, ticket: Ticket, team: Team) -> Ticket_Team_Assignment:
    
            assignment = Ticket_Team_Assignment.objects.create(
                Ticket=ticket,
                Team=team
            )
            return assignment
 
    
    def assign_ticket_to_user(self, Ticket: Ticket, User:CustomUser ) -> Ticket_User_Assignment:
    
            assignment = Ticket_User_Assignment.objects.create(
                Ticket=Ticket,
                user=User
            )
            assignment.save()
            return assignment 
    

    def get_ticket_assign_to_user(self,user_id) ->  QuerySet:
      
        return Ticket.objects.filter(ticket_user_assignment__user_id=user_id)

    
    def get_ticket_assign_to_team(self,team_id) ->  QuerySet: 
        return  Ticket.objects.filter(ticket_team_assignment__Team_id=team_id)
    
    def update_ticket(self, ticket: Ticket, updated_data: dict) -> Ticket:
        for attr, value in updated_data.items():
            setattr(ticket, attr, value)
        ticket.save()
        return ticket

    def delete_ticket(self, ticket: Ticket) -> None:
        ticket.delete()   
   
