from django.urls import path

from .views import TicketAnalyzeView

urlpatterns = [
    path("analyze", TicketAnalyzeView.as_view(), name="ticket-analyze"),
]
