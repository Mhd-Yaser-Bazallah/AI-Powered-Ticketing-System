                          
from django.urls import path
from . import views

urlpatterns = [
                                         
    path('List', views.ListUsersView.as_view(), name='user-list'),             
    path('create', views.CreateUserView.as_view(), name='user-create'),      
    path('update/<int:user_id>', views.UpdateUserView.as_view(), name='user-update'), 
    path('delete/<int:user_id>', views.DeleteUserView.as_view(), name='user-delete'),  
    path('search/<int:user_id>', views.SearchUserView.as_view(), name='user-search'),   
    path('getme/<int:user_id>', views.getMeView.as_view(), name='GetMe'),
    path('account/update', views.AccountUpdateView.as_view(), name='account-update'),    
    path('account/delete', views.AccountUpdateView.as_view(), name='account-delete'),    
    ]
