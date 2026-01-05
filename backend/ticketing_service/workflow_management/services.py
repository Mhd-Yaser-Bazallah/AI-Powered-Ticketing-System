from .repositories import WorkflowRepository
from users_management.repositories import UserRepository
from company.models import Company
from injector import inject

class WorkflowService:
    @inject
    def __init__(self, repo: WorkflowRepository, user_repo: UserRepository):
        self.repo = repo
        self.user_repo = user_repo


    def create_default_workflow_for_company(self, company: Company, created_by):
        default_workflow = self.repo.create_workflow("Default Workflow", company=company, created_by=created_by)
        step_names = ["open", "Assign to Team", "Assign to Member", "In Progress", "Done"]
        for index, name in enumerate(step_names):
            self.repo.create_step(default_workflow, name, index)
        return default_workflow

    def list_all_workflows(self):
        return self.repo.list_workflows()

    def get_workflow_by_company(self, company: Company):
        return self.repo.get_workflow_by_company(company)

    def create_custom_workflow(self, name: str, steps: list, company: Company, created_by):
        workflow = self.repo.create_workflow(name=name, company=company, created_by=created_by)
        for index, step in enumerate(steps):
            self.repo.create_step(workflow, step, index)
        return workflow
    