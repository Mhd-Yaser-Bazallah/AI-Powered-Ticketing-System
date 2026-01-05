from .models import Workflow, WorkflowStep
from injector import inject
from typing import List, Optional

class WorkflowRepository:
    @inject
    def __init__(self):
        pass

    def create_workflow(self, name: str, company=None, created_by=None) -> Workflow:
        return Workflow.objects.create(name=name, company=company, created_by=created_by)

    def create_step(self, workflow: Workflow, name: str, order: int) -> WorkflowStep:
        return WorkflowStep.objects.create(workflow=workflow, name=name, order=order)

    def get_workflow_by_company(self, company) -> Optional[Workflow]:
        return Workflow.objects.filter(company=company).first()

    def get_global_workflow(self) -> Optional[Workflow]:
        return Workflow.objects.filter(company=None).first()

    def list_workflows(self) -> List[Workflow]:
        return Workflow.objects.all()

    def get_steps_for_workflow(self, workflow: Workflow) -> List[WorkflowStep]:
        return list(WorkflowStep.objects.filter(workflow=workflow).order_by('order'))
