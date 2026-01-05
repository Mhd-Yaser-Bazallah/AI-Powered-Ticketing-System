from django.urls import path
from .views import CompanyAnalysisView

urlpatterns = [
    path('analysis/<int:company_id>/', CompanyAnalysisView.as_view(), name='company-analysis'),
]