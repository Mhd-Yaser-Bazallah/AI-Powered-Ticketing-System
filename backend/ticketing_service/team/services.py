from injector import inject

from users_management.models import Membership
from users_management.repositories import UserRepository
from users_management.services import UserService
from .repositories import TeamRepository
from rest_framework.exceptions import NotFound
from .models import Team
from users_management.models   import CustomUser
class TeamService:
    @inject
    def __init__(self, TeamRepository: TeamRepository):
        self.TeamRepository = TeamRepository
        self.user_repo = UserRepository
       
    def list_team(self):
        return self.TeamRepository.get_all_Team()
    
    def list_team_No_page(self,company):
        return self.TeamRepository.get_all_Team_company(company)

    def create_team(self, category, description, company):
        try:
        
            return self.TeamRepository.create_Team(category=category, description=description, company=company)
        except Exception as e:
            raise e
        
    def get_team_members_by_company_id(self,company_id):
        return self.user_repo.get_team_members_by_company(company_id)

    def update_team(self, team_id, validated_data):
        try:
            team= self.TeamRepository.get_Team_by_id(team_id)
            
        except Team.DoesNotExist:
            raise NotFound("Team not found")
        return self.TeamRepository.update_team(team, validated_data)

    def delete_team(self, team_id):
        try:
            
            team = self.TeamRepository.get_Team_by_id(team_id)
        
        except Team.DoesNotExist:
            raise NotFound("Team not found")
        self.TeamRepository.delete_team(team)    

    def search_team(self, team_id):
        try:
             team= self.TeamRepository.get_Team_by_id(team_id)
        except Team.DoesNotExist:
            raise NotFound("Team not found")
        return team
    
    
    def add_user_to_team(self, user_id: int, team_id: int) -> Membership:
 
  
        try:
   
            user = self.user_repo.get_user_by_id(self,user_id)       
        except CustomUser.DoesNotExist:
         
            raise NotFound(f"User with ID {user_id} not found.")
        try:    
    
            team = self.TeamRepository.get_Team_by_id(team_id)   
            return self.TeamRepository.add_user_to_team(user, team)
        except Team.DoesNotExist:
            raise NotFound(f"Team with ID {team_id} not found.")
