from django.urls import path
from . import views

urlpatterns = [
                                        
    path('<int:user_id>/', views.NotificationListView.as_view(), name='notifications-list'),

                              
    path('<int:notification_id>/read/', views.MarkAsReadView.as_view(), name='notification-mark-read'),

                                 
    path('read/all/', views.MarkAllAsReadView.as_view(), name='notifications-mark-all-read'),
]
