from ticket.models import Ticket, Ticket_Team_Assignment, Ticket_User_Assignment
from team.models import Team
from users_management.models import CustomUser
from django.db.models import Count

class AnalysisRepository:
    
    def get_total_tickets(self, company_id: int) -> int:
        return Ticket.objects.filter(company_id=company_id).count()
    
    def get_tickets_by_status(self, company_id: int):
        return Ticket.objects.filter(company_id=company_id).values('status').annotate(count=Count('id'))
    
    def get_assigned_vs_unassigned(self, company_id: int):
        assigned_ticket_ids = Ticket_User_Assignment.objects.filter(Ticket__company_id=company_id).values_list('Ticket_id', flat=True).distinct()
        total_tickets = Ticket.objects.filter(company_id=company_id).count()
        assigned_count = len(assigned_ticket_ids)
        unassigned_count = total_tickets - assigned_count
        return {"assigned": assigned_count, "unassigned": unassigned_count}
    
    def get_tickets_by_team(self, company_id: int):
        return (
            Ticket_Team_Assignment.objects
            .filter(Ticket__company_id=company_id)
            .values('Team__category')
            .annotate(count=Count('Ticket'))
            .order_by('-count')
        )
    
    def get_tickets_by_user(self, company_id: int):
        return (
            Ticket_User_Assignment.objects
            .filter(Ticket__company_id=company_id)
            .values('user__username')
            .annotate(count=Count('Ticket'))
            .order_by('-count')
        )
