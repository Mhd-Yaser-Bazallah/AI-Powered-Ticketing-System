from ticket.models import Ticket, Ticket_User_Assignment
from django.db.models import Count, Avg, F
from django.utils.timezone import now

class ReportRepository:
    def tickets_by_status(self):
        return Ticket.objects.values("status").annotate(total=Count("id"))

    def tickets_by_priority(self):
        return Ticket.objects.values("priority").annotate(total=Count("id"))

    def team_performance(self):
        return Ticket_User_Assignment.objects.values(
            team_name=F("user__membership__team_id__category"),
            user_email=F("user__email")
        ).annotate(total=Count("Ticket__id"))

    def company_tickets(self):
        return Ticket.objects.values("company__name").annotate(total=Count("id"))
