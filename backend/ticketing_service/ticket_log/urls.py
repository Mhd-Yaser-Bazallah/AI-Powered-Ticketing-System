                          
from django.urls import path
from . import views

urlpatterns = [
                                         
       
    path('List', views.ListLogView.as_view(), name='log-list'),                                  
    path('create', views.CreateLogView.as_view(), name='log-create'),
    path('cmopany_log/<int:company_id>', views.ListLogCompanyView.as_view(), name='log-create'),                               
    path('search/<int:log_id>', views.SearchLogView.as_view(), name='log-search'),                        
    ]
