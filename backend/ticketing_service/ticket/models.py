                  
from users_management.models import CustomUser
from company.models import Company
from django.db import models
from django.conf import settings
from team.models import Team
# from ticket.utils.ml.inference.ticket_router import router

class Ticket(models.Model): 
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(CustomUser,related_name='create_ticket', on_delete=models.CASCADE)
    company = models.ForeignKey(Company,blank=True, null=True, on_delete=models.CASCADE)
    title = models.TextField(default="ticket")
    status = models.CharField(max_length=50 ,default="open")
    category = models.CharField(max_length=50,default="back")
    priority =models.CharField(max_length=50,default="low") 
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
                                   
    solution_steps = models.JSONField(null=True, blank=True)
    solution_confidence = models.FloatField(null=True, blank=True)
    human_solution_steps = models.JSONField(null=True, blank=True)
    human_solved_at = models.DateTimeField(null=True, blank=True)
    human_solved_by = models.ForeignKey(
        CustomUser,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="human_solved_tickets",
    )                                     
    bert_category = models.CharField(max_length=255, null=True, blank=True)
    bert_confidence = models.FloatField(null=True, blank=True)
    similarity_score = models.FloatField(null=True, blank=True)                                                    
    need_admin = models.BooleanField(default=False)


    def __str__(self):
        return f"Ticket {self.id} - {self.status}"
    class Meta:
        db_table = 'Ticket'
 
 
class Ticket_Team_Assignment(models.Model):
    Team  = models.ForeignKey(Team, on_delete=models.CASCADE)
    Ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    assigen_at = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'Ticket_Team_Assignment' 

class Ticket_User_Assignment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Ticket= models.ForeignKey(Ticket, on_delete=models.CASCADE)
    assigen_at = models.DateField(auto_now=True)


    def __str__(self):
        return f"Assignment {self.id} - Ticket {self.Ticket.id} to User {self.user.id}"    
    
    class Meta:
        db_table = 'Ticket_User_Assignment'
