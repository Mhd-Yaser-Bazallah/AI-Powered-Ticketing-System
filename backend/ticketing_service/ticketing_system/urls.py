from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('authentication/', include('authentication.urls')),
    path('users/', include('users_management.urls')),
    path('notification/', include('notification.urls')),
    path('company/', include('company.urls')),
    path('team/', include('team.urls')),
    path('ticket/', include('ticket.urls')),
    path('ticket-log/', include('ticket_log.urls')),
    path('comments/', include('comments.urls')),
    path('workflow/', include('workflow_management.urls')),
    path('reporting/', include('reporting.urls')),
    path('analysis/', include('analysis.urls')),
    path('api/files/', include('files.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
