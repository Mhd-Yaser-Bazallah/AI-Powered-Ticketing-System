 
from injector import inject
from .models import TicketLog  
from django.core.exceptions import ObjectDoesNotExist 
from django.db.models import QuerySet

class ticketLogRepository:
    @inject

    def create_ticketLog(self, ticket: int, user: int, action: str,previous_status:str , new_status:str ,comments : str,company:int) -> TicketLog:
        ticketLog = TicketLog(ticket_id=ticket, user_id=user, action=action ,
                               previous_status=previous_status, new_status=new_status , comments=comments,company_id=company)
        
        ticketLog.save()
        
        return ticketLog
     
    def get_all_ticket_company(self ,company)-> QuerySet:
        return TicketLog.objects.filter(company_id =company).order_by('created_at')
    def get_all_ticketLog(self) -> QuerySet:
        return TicketLog.objects.all().order_by('created_at')
    
 
    
    def get_ticketLog_by_id(self, log_id: int) -> TicketLog:
        return TicketLog.objects.all(log_id=log_id)
         
        
     
