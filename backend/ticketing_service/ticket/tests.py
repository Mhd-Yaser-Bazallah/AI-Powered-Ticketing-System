import os

import jwt
from django.test import TestCase
from rest_framework.test import APIClient

from company.models import Company
from users_management.models import CustomUser
from workflow_management.repositories import WorkflowRepository
from ticket.models import Ticket


class SolveTicketTests(TestCase):
    def setUp(self):
        os.environ["JWT_SECRET"] = "test-secret"
        self.client_api = APIClient()
        self.company = Company.objects.create(name="Acme", address="A", email="a@a.com")
        self.client_user = CustomUser.objects.create(
            email="client@a.com",
            username="client",
            company_id=self.company,
            role="client",
            password="x",
        )
        self.support_user = CustomUser.objects.create(
            email="support@a.com",
            username="support",
            company_id=self.company,
            role="support_team_member",
            password="x",
        )
        workflow_repo = WorkflowRepository()
        workflow = workflow_repo.create_workflow(name="wf", company=self.company)
        workflow_repo.create_step(workflow, name="open", order=1)
        workflow_repo.create_step(workflow, name="done", order=2)
        self.ticket = Ticket.objects.create(
            client=self.client_user,
            company=self.company,
            title="t1",
            description="desc",
            status="open",
        )

    def _token(self, role: str) -> str:
        payload = {"role": role}
        return jwt.encode(payload, os.environ["JWT_SECRET"], algorithm="HS256")

    def test_unauthorized_role_blocked(self):
        token = self._token("client")
        res = self.client_api.post(
            f"/ticket/{self.ticket.id}/solve",
            {"steps": ["one"]},
            format="json",
            HTTP_AUTHORIZATION=f"Bearer={token}",
        )
        self.assertIn(res.status_code, (401, 403))

    def test_solve_ticket_transitions_and_saves_steps(self):
        token = self._token("support_team_member")
        res = self.client_api.post(
            f"/ticket/{self.ticket.id}/solve",
            {"steps": ["step 1", "step 2"], "user_id": self.support_user.id},
            format="json",
            HTTP_AUTHORIZATION=f"Bearer={token}",
        )
        self.assertEqual(res.status_code, 200)

        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, "done")
        self.assertEqual(
            self.ticket.human_solution_steps,
            [{"order": 1, "text": "step 1"}, {"order": 2, "text": "step 2"}],
        )
