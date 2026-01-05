                          
from django.urls import path
from . import views

urlpatterns = [ 
    path('List', views.ListTeamView.as_view(), name='team-list'),
    path('List-members/<int:company_id>', views.listTeamMembersInCompany.as_view(), name='team-members-list'),
    path('team/<int:company_id>', views.ListTeamNoPageView.as_view(), name='team-list-no-page'),                  
    path('create', views.CreateTeamView.as_view(), name='team-create'),
    path('createMember', views.CreateTeamMemberView.as_view(), name='team-member-create'),      
    path('update/<int:team_id>', views.UpdateTeamrView.as_view(), name='team-update'),    
    path('delete/<int:team_id>', views.DeleteTeamView.as_view(), name='team-delete'),   
    path('search/<int:team_id>', views.SearchTeamView.as_view(), name='team-search'),    
    path('add-user/<int:user_id>', views.AddUserToTeamView.as_view(), name='add-user-to-team'),
    path('activate/<int:user_id>', views.ActivateMembmeView.as_view(), name='activate-user'),
    path('deactivate/<int:user_id>', views.DeActivateMembmeView.as_view(), name='activate-user'),
    ]
