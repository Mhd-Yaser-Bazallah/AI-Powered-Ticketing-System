from injector import inject
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users_management.permissions import IsAdmin

from .services import ReportService
from .repositories import ReportRepository
from .utils import export_to_excel


class BaseReportView(APIView):
    @inject
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ReportService = ReportService(ReportRepository())


class TicketStatusReportView(BaseReportView):
                                    

    def get(self, request):
        try:
            headers, rows, filename = self.ReportService.get_ticket_status_report()
            return export_to_excel(headers, rows, filename)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TicketPriorityReportView(BaseReportView):
                                    

    def get(self, request):
        try:
            headers, rows, filename = self.ReportService.get_ticket_priority_report()
            return export_to_excel(headers, rows, filename)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TeamPerformanceReportView(BaseReportView):
                                    

    def get(self, request):
        try:
            headers, rows, filename = self.ReportService.get_team_performance_report()
            return export_to_excel(headers, rows, filename)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CompanyTicketsReportView(BaseReportView):
                                    

    def get(self, request):
        try:
            headers, rows, filename = self.ReportService.get_company_tickets_report()
            return export_to_excel(headers, rows, filename)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
