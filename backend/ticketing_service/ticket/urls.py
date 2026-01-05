                          
from django.urls import path
from . import views

urlpatterns = [
                                         
    path('List', views.ListTicketView.as_view(), name='ticket-list'),                 
    path('create', views.CreateTicketView.as_view(), name='ticket-create'),      
    path('client-Tickets/<int:client_id>', views.ClientTicketView.as_view(), name='ticket-by-client_id'),
    path('assign-user-Tickets/<int:user_id>', views.GetTicketAssignToMeView.as_view(), name='ticket-assign-user_id'),
    path('assign-team-Tickets/<int:team_id>', views.GetTicketAssignToTeamView.as_view(), name='ticket-assign-team_id'),
    path('company-Tickets/<int:company_id>', views.CompanyTicketView.as_view(), name='ticket-by-company_id'),
    path('Assign-Ticket-team/<int:ticket_id>', views.AssignTicketToTeamView.as_view(), name='ticket-assign-team_id'),
    path('Ticket-In-Progress/<int:ticket_id>', views.TicketToInProgressView.as_view(), name='ticket-To-In Progress'),
    path('Ticket-To-Done/<int:ticket_id>', views.TicketToDoneView.as_view(), name='ticket-To-Done'),
    path('Assign-Ticket-user/<int:ticket_id>', views.AssignTicketToMeView.as_view(), name='ticket-assign-user_id'),
    path('update/<int:ticket_id>', views.UpdateTicketView.as_view(), name='team-update'),   
    path('delete/<int:ticket_id>', views.DeleteTicketView.as_view(), name='team-delete'),   
    path('<int:ticket_id>/advance-status', views.AdvanceTicketStatusView.as_view(), name='advance-ticket-status'),
    path('<int:ticket_id>/solve', views.SolveTicketView.as_view(), name='solve-ticket'),

    ]
