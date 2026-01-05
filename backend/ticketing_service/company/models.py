from django.db import models

class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    auto_prioritize = models.BooleanField(default=True)   
    auto_categorize = models.BooleanField(default=True)   
    auto_assign = models.BooleanField(default=True)   
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Company'