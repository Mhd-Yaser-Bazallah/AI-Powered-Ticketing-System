from .repositories import ReportRepository
from injector import inject

class ReportService:
    @inject
    def __init__(self,Report_Repository:ReportRepository):
        self.repo = Report_Repository

 

    def get_ticket_status_report(self):
        data = self.repo.tickets_by_status()
        headers = ["Status", "Total"]
        rows = [(d["status"], d["total"]) for d in data]
        return headers, rows, "ticket_status_report.xlsx"

    def get_ticket_priority_report(self):
        data = self.repo.tickets_by_priority()
        headers = ["Priority", "Total"]
        rows = [(d["priority"], d["total"]) for d in data]
        return headers, rows, "ticket_priority_report.xlsx"

    def get_team_performance_report(self):
        data = self.repo.team_performance()
        headers = ["Team", "User", "Total Tickets"]
        rows = [(d["team_name"], d["user_email"], d["total"]) for d in data]
        return headers, rows, "team_performance_report.xlsx"

    def get_company_tickets_report(self):
        data = self.repo.company_tickets()
        headers = ["Company", "Total Tickets"]
        rows = [(d["company__name"], d["total"]) for d in data]
        return headers, rows, "company_tickets_report.xlsx"
