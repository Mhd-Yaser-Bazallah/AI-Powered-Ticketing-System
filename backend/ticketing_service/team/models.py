from django.db import models
from company.models import Company
 
class Team(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, blank=True, null=True,on_delete=models.CASCADE)
    category = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
                           
    embedding = models.JSONField(null=True, blank=True)
    def __str__(self):
        return f"{self.company.name if self.company else 'No Company'} - {self.category}"
    
    class Meta:
        db_table = 'Team'