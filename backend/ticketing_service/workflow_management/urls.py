from django.urls import path
from .views import CreateCompanyDefaultWorkflowView, GetWorkflowByCompanyView, ListWorkflowView, CreateDefaultWorkflowView, CreateCustomWorkflowView

urlpatterns = [
    path('list', ListWorkflowView.as_view(), name='list-workflows') ,
    path('create', CreateCustomWorkflowView.as_view(), name='create-custom-workflow'),
    path('create-default-company', CreateCompanyDefaultWorkflowView.as_view(), name='create-default-company-workflow'),
     path('by-company', GetWorkflowByCompanyView.as_view(), name='workflow-by-company'),
]
