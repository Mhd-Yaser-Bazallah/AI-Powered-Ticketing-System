from datetime import timezone
from django.db import models 
from django.contrib.auth.hashers import make_password
from company.models import Company
from team.models import Team

class CustomUser(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('client', 'Client'),
        ('support_team_member', 'Support Team Member'),
        ('support_team_manager', 'Support Team Manager'),
    )

    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255)  
    company_id = models.ForeignKey(Company,blank=True, null=True,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES,default='client')
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=128)  
    active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def set_password(self, raw_password):
          self.password = make_password(raw_password)
 
    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'customuser'

class Membership(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    date_joined = models.DateField()
    
    class Meta:
        db_table = 'Membership'