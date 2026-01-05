from django.db import models
from ticket.models import Ticket
from users_management.models import CustomUser
from django.utils import timezone

class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f"Comment {self.id} on Ticket {self.ticket.id}"
    
    class Meta:
        db_table = 'Comments' 
        ordering = ['created_at']