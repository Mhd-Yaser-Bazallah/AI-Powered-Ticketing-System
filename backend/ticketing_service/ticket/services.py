from injector import inject

from company.models import Company
from users_management.models import Membership
from users_management.repositories import UserRepository
from users_management.services import UserService
from .repositories import TicketRepository

from rest_framework.exceptions import NotFound
from .models import Ticket
from users_management.models   import CustomUser
from team.repositories import TeamRepository
from team.models import Team

from ticket_log.repositories import ticketLogRepository    
    
class TicketService:
    @inject
    def __init__(self, TicketRepository: TicketRepository,TeamRepository:TeamRepository):
        self.TicketRepository = TicketRepository
        self.user_repo = UserRepository
        self.TeamRepository = TeamRepository
        self.ticketLogRepository=ticketLogRepository
         

    def list_ticket(self):
        return self.TicketRepository.get_all_ticket()

    def create_ticket(self, description, title, company_id, client_id,priority,category,status):
        try: 
            
            ticket= self.TicketRepository.create_ticket(client_id, company_id, title, description,priority,category,status)
            return ticket
        except CustomUser.DoesNotExist:
            raise NotFound(f"Client with ID {client_id} not found.")
        except Company.DoesNotExist:
            raise NotFound(f"Company with ID {company_id} not found.")
    

    def client_tickets(self,client_id):
        return self.TicketRepository.get_client_tickets(client_id)    
 

    
    def company_tickets(self,company_id):
        return self.TicketRepository.get_company_tickets(company_id)    
    
    def ticket_assign_to_user(self,user_id):
        return self.TicketRepository.get_ticket_assign_to_user(user_id)    
    

    def ticket_assign_to_team(self,team_id):
        return self.TicketRepository.get_ticket_assign_to_team(team_id)    


    def assign_ticket_to_team(self, ticket_id: int, team_id: int):
       
        try:
            team = self.TeamRepository.get_Team_by_id(team_id)
        except Team.DoesNotExist:
            raise NotFound(f"Team with ID {team_id} not found.")

       
        try:
            ticket = self.TicketRepository.get_ticket_by_id(ticket_id)
        except Ticket.DoesNotExist:
            raise NotFound(f"Ticket with ID {ticket_id} not found.")
 
        return self.TicketRepository.assign_ticket_to_team(ticket, team)
       

    def assign_ticket_to_user(self, ticket_id: int, user_id: int):
 
        try:
            user = self.user_repo.get_user_by_id(self ,user_id)
      
        except CustomUser.DoesNotExist:
            raise NotFound(f"User with ID {user_id} not found.")

 
        try:
            ticket = self.TicketRepository.get_ticket_by_id(ticket_id)
        except Ticket.DoesNotExist:
            raise NotFound(f"Ticket with ID {ticket_id} not found.")
         
 
        return self.TicketRepository.assign_ticket_to_user(ticket,user)
        


    def update_ticket(self, ticket_id:int, validated_data):
        try:
            ticket= self.TicketRepository.get_ticket_by_id(ticket_id)
            
        except Ticket.DoesNotExist:
            raise NotFound("Ticket not found")
        return self.TicketRepository.update_ticket(ticket, validated_data)

    def delete_ticket(self, ticket_id:int):
        try:
            ticket= self.TicketRepository.get_ticket_by_id(ticket_id)
        except Ticket.DoesNotExist:
            raise NotFound("ticket not found")
        self.TicketRepository.delete_ticket(ticket)    
