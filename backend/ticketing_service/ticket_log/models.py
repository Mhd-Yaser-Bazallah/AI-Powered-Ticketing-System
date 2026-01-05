from django.db import models
from company.models import Company
from ticket.models import Ticket
from users_management.models import CustomUser
from comments.models import Comments
class TicketLog(models.Model):
    id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    company = models.ForeignKey(Company,blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=255)
    previous_status = models.CharField(max_length=50)
    new_status = models.CharField(max_length=50)
    comments = models.CharField(max_length=50)
    
    def __str__(self):
        return f"Log {self.id} for Ticket {self.ticket.id}"
    
    class Meta:
        db_table = 'TicketLog'