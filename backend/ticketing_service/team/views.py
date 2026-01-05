from injector import inject 
from rest_framework.views import APIView

from ticket.team_embedding import update_team_embedding
from users_management.models import CustomUser
from users_management.serializers import TeamMemberSerializer, UserCreateUpdateSerializer, UserSerializer
from users_management.services import UserService
from users_management.repositories import UserRepository
from .services import TeamService
from .repositories import TeamRepository
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from users_management.permissions import IsAdmin, IsSupportTeamManager 
from .serializers import TeamSerializer ,TeamCreateUpdateSerializer

class BaseTeamView(APIView):
    @inject
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.teamService = TeamService(TeamRepository())
        self.UserService=UserService(UserRepository())

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


class CreateTeamMemberView(BaseTeamView):
                                                 

    def post(self, request):
        serializer = UserCreateUpdateSerializer(data=request.data)
         
        if serializer.is_valid():
            try:
                user_data = self.UserService.create_Team_member(serializer.validated_data)
                serialized_user = UserSerializer(user_data).data
                return Response(serialized_user, status=status.HTTP_201_CREATED)
            except Exception as e:
                 return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListTeamView(BaseTeamView):
   
                                                  
    pagination_class = CustomPagination

    
    def get(self, request):
     
        team = self.teamService.list_team()
        paginator = self.pagination_class()
        paginated_team = paginator.paginate_queryset(team, request)
        return paginator.get_paginated_response(TeamSerializer(paginated_team, many=True).data)

class listTeamMembersInCompany(BaseTeamView):
                                                 
    pagination_class = CustomPagination

    def get(self, request, company_id):
        try:
             
            members = self.teamService.get_team_members_by_company_id(company_id)

             
            paginator = self.pagination_class()
            paginated_team = paginator.paginate_queryset(members, request)

             
            serialized_data = TeamMemberSerializer(paginated_team, many=True).data
            return paginator.get_paginated_response(serialized_data)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
class ListTeamNoPageView(BaseTeamView):
                                                  
 
     
    def get(self, request,company_id):
        team = self.teamService.list_team_No_page(company_id)
        serialized_data = TeamSerializer(team, many=True)
                                                       
        return Response(serialized_data.data, status=200)

        
 
class CreateTeamView(BaseTeamView):
    permission_classes = [IsSupportTeamManager]

    def post(self, request):
        serializer = TeamCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
                    try:
                        validated_data = serializer.validated_data
                    
                        company = validated_data['company']  
                        category = validated_data['category']       
                        description = validated_data['description']   
                        
                        team_data = self.teamService.create_team(description=description, category=category, company=company)

                         
                        serialized_team = TeamSerializer(team_data).data
                        return Response(serialized_team, status=status.HTTP_201_CREATED)
                    except Exception as e:
                        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateTeamrView(BaseTeamView):
                                                 

    def put(self, request, team_id):
        serializer = TeamCreateUpdateSerializer(data=request.data,partial=True)
        
        if serializer.is_valid():
        
            updated_team = self.teamService.update_team(team_id, serializer.validated_data)
            update_team_embedding(team_id)
            
            serialized_team =TeamSerializer(updated_team).data
            return Response(serialized_team, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteTeamView(BaseTeamView):
    permission_classes = [IsSupportTeamManager]

    def delete(self, request, team_id):
        self.teamService.delete_team(team_id)
        return Response(status=status.HTTP_200_OK)

class SearchTeamView(BaseTeamView):
    permission_classes = [IsSupportTeamManager]

    def get(self, request, team_id=None):
 
        if team_id:
            team = self.teamService.search_team(team_id)
 
            if team:
 
                team_serializer =TeamSerializer(team)
                return Response(team_serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "team not found."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"error": "team  ID is required."}, status=status.HTTP_400_BAD_REQUEST)
    
class AddUserToTeamView(BaseTeamView):
    permission_classes = [IsSupportTeamManager]

    def post(self, request, user_id):
        team_id = request.data.get("team_id") 
        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            membership = self.teamService.add_user_to_team(user_id=user_id, team_id=team_id)
            return Response(
                {"message": f"User {membership.user_id.email} added to team {membership.team_id.category} successfully."},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ActivateMembmeView(BaseTeamView):
    permission_classes = [IsSupportTeamManager]

    def put(self, request, user_id):
        try:
 
            user = self.UserService.user_repo.get_user_by_id(user_id)
 
            updated_user = self.UserService.user_repo.update_user(user, {"active": True})
 
            return Response(
                {"message": "User activated successfully", "user_id": updated_user.id},
                status=status.HTTP_200_OK
            )
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class DeActivateMembmeView(BaseTeamView):
    permission_classes = [IsSupportTeamManager]

    def put(self, request, user_id):
        try: 
            user = self.UserService.user_repo.get_user_by_id(user_id)
 
            updated_user = self.UserService.user_repo.update_user(user, {"active": False})
 
            return Response(
                {"message": "User dractivated successfully", "user_id": updated_user.id},
                status=status.HTTP_200_OK
            )
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )        
