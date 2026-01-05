                          
from django.urls import path
from . import views

urlpatterns = [
   
    path('List', views.ListCompanyView.as_view(), name='company-list'),
    path('company', views.ListCompanyNoPageView.as_view(), name='company-list'),  
    path('create', views.CreateCompanyView.as_view(), name='company-create'),     
    path('update/<int:company_id>', views.UpdateCompanyrView.as_view(), name='company-update'),  
    path('delete/<int:company_id>', views.DeleteCompanyView.as_view(), name='company-delete'),   
    path('search/<int:company_id>', views.SearchCompanyView.as_view(), name='company-search'),    
    path('company_email', views.GetCompanyByEmailView.as_view(), name='company-list'), 
    path('toggle_auto_prioritize/<int:company_id>/', views.ToggleAutoPrioritizeView.as_view(), name='toggle-auto-prioritize'),
    path('toggle_auto_categorize/<int:company_id>/', views.ToggleAutoCategorizeView.as_view(), name='toggle-auto-categorize'),
    path('toggle_auto_assign/<int:company_id>/', views.ToggleAutoAssignView.as_view(), name='toggle-auto-categorize'),
    ]
