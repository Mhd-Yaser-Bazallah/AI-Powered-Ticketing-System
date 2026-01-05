from django.urls import path
from . import views

urlpatterns = [
    path("", views.FileListCreateView.as_view(), name="files-list-create"),
    path("<uuid:file_id>/", views.FileDeleteView.as_view(), name="files-delete"),
]
