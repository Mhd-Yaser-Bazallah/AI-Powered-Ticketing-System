                        
from django.db import models
from users_management.models import CustomUser
from company.models import Company
from ticket.models import Ticket

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Notification"

    def __str__(self):
        return f"To: {self.recipient.email} | {self.message[:50]}"
