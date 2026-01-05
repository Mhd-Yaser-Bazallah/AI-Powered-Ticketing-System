                    
from django.db import models
from company.models import Company
from users_management.models import CustomUser

class Workflow(models.Model):
    name = models.CharField(max_length=255, default="Default Workflow")
    company = models.OneToOneField(Company, on_delete=models.CASCADE, null=True, blank=True, related_name='workflow')
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.company.name if self.company else 'Global'}"

    class Meta:
        db_table = 'workflow'

class WorkflowStep(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='steps')
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.workflow.name} Step {self.order}: {self.name}"

    class Meta:
        db_table = 'workflow_step'
        ordering = ['order']
        unique_together = ['workflow', 'order']
