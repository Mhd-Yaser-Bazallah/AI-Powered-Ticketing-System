 
from injector import inject

from ticket.team_embedding import update_team_embedding
from .models import Team  
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from users_management.models import Membership ,CustomUser 
from datetime import date

class TeamRepository:
    @inject

    def create_Team(self ,category: str, description: str, company: str) -> Team:
        team = Team(category=category, description=description, company=company)
        
        team.save()
        update_team_embedding(team) 

        return team
    
    def add_user_to_team(self, user: CustomUser, team: Team) -> Membership:
        membership = Membership(
            user_id=user,
            team_id=team,
            date_joined=date.today()
        )
        membership.save()
        return membership

    def get_all_Team(self) -> QuerySet:
        return Team.objects.all().order_by('created_at')


    def get_all_Team_company(self,company) -> QuerySet:
            return Team.objects.filter(company=company).order_by('created_at')


    def get_Team_by_id(self,team_id: int) -> Team:
        return Team.objects.get(id=team_id)
         
        
    def update_team(self, team: Team, updated_data: dict) -> Team:
        for attr, value in updated_data.items():
            setattr(team, attr, value)
        team.save()
        return team

    def delete_team(self, team: Team) -> None:
        team.delete()   
   
