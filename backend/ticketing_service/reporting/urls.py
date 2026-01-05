from django.urls import path
from . import views

urlpatterns = [
    path('tickets/status', views.TicketStatusReportView.as_view(), name='ticket-status-report'),
    path('tickets/priority', views.TicketPriorityReportView.as_view(), name='ticket-priority-report'),
    path('teams/performance', views.TeamPerformanceReportView.as_view(), name='team-performance-report'),
    path('companies/tickets', views.CompanyTicketsReportView.as_view(), name='company-tickets-report'),
]
