from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from injector import inject
from .services import AnalysisService
from .repositories import AnalysisRepository
from .serializers import AnalysisSerializer
from users_management.permissions import IsAdmin, IsSupportTeamManager

class CompanyAnalysisView(APIView):
                                                           

    @inject
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.analysisService = AnalysisService(AnalysisRepository())

    def get(self, request, company_id):
        try:
            analytics = self.analysisService.get_company_analytics(company_id)
            serializer = AnalysisSerializer(analytics)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
