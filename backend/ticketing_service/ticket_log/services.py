from injector import inject
 
from .repositories import ticketLogRepository
from rest_framework.exceptions import NotFound
from .models import TicketLog

class TicketLogService:
    @inject
    def __init__(self, ticketLogRepository: ticketLogRepository):
        self.ticketLogRepository = ticketLogRepository
   
    def list_log(self):
        return self.ticketLogRepository.get_all_ticketLog()

    def list_log_company(self,company_id):
        return self.ticketLogRepository.get_all_ticket_company(company_id)
    
    
    def create_log(self,  ticket, user , action ,previous_status , new_status, comments,company):
        try:
            
            
            return self.ticketLogRepository.create_ticketLog( ticket=ticket, 
                                                             user=user, action=action ,
                                                             previous_status=previous_status 
                                                             , new_status= new_status ,comments=comments,company=company)
        except Exception as e:
            raise e
    
    def search_log(self, log_id):
        try:
             log= self.ticketLogRepository.get_ticketLog_by_id(log_id)
        except TicketLog.DoesNotExist:
            raise NotFound("log not found")
        return log
     