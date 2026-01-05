from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import WorkflowSerializer
from .services import WorkflowService
from rest_framework import status

class BaseWorkflowView(APIView): 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from .repositories import WorkflowRepository
        from users_management.repositories import UserRepository
        self.workflow_service = WorkflowService(WorkflowRepository(), UserRepository())

class ListWorkflowView(BaseWorkflowView):
    def get(self, request):
        workflows = self.workflow_service.list_all_workflows()
        serialized = WorkflowSerializer(workflows, many=True)
        return Response(serialized.data, status=200)

class CreateDefaultWorkflowView(BaseWorkflowView):
    def post(self, request):
        workflow = self.workflow_service.create_default_workflow()
        serialized = WorkflowSerializer(workflow)
        return Response(serialized.data, status=201)

class CreateCustomWorkflowView(BaseWorkflowView):
    def post(self, request):
        serializer = WorkflowSerializer(data=request.data)
        if serializer.is_valid():
            workflow = serializer.save()
            return Response(WorkflowSerializer(workflow).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CreateCompanyDefaultWorkflowView(BaseWorkflowView):
    def post(self, request):
        company_id = request.data.get('company')
        created_by_id = request.data.get('created_by')
        if not company_id or not created_by_id:
            return Response({"error": "company and created_by are required"}, status=400)

        from company.models import Company
        from users_management.models import CustomUser

        try:
            company = Company.objects.get(id=company_id)
            created_by = CustomUser.objects.get(id=created_by_id)
        except (Company.DoesNotExist, CustomUser.DoesNotExist):
            return Response({"error": "Company or User not found"}, status=404)

        workflow = self.workflow_service.create_default_workflow_for_company(company=company, created_by=created_by)
        return Response(WorkflowSerializer(workflow).data, status=201)
class GetWorkflowByCompanyView(BaseWorkflowView):
    def get(self, request):
        company_id = request.query_params.get('company_id')
        if not company_id:
            return Response({"error": "company_id is required as a query param"}, status=400)

        from company.models import Company
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=404)

        workflow = self.workflow_service.get_workflow_by_company(company)
        if not workflow:
            return Response({"message": "No workflow found for this company"}, status=404)

        return Response(WorkflowSerializer(workflow).data, status=200)