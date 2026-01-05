from injector import inject
from .repositories import AnalysisRepository

class AnalysisService:
    @inject
    def __init__(self, repo: AnalysisRepository):
        self.repo = repo

    def get_company_analytics(self, company_id: int):
        total = self.repo.get_total_tickets(company_id)
        by_status = list(self.repo.get_tickets_by_status(company_id))
        assigned = self.repo.get_assigned_vs_unassigned(company_id)
        by_team = list(self.repo.get_tickets_by_team(company_id))
        by_user = list(self.repo.get_tickets_by_user(company_id))

        return {
            "total_tickets": total,
            "tickets_by_status": by_status,
            "assigned_vs_unassigned": assigned,
            "tickets_by_team": by_team,
            "tickets_by_user": by_user,
        }
