from injector import inject 
from rest_framework.views import APIView

                         
from .services import CompanyService
from .repositories import CompanyRepository
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from users_management.permissions import IsAdmin, IsSupportTeamManager, IsUser
from .serializers import CompanyCreateUpdateSerializer , CompanySerializer

class BaseCompanyView(APIView):
    @inject
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.CompanyService = CompanyService(CompanyRepository())

class CustomPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
         
        total_pages = (self.page.paginator.count + self.page_size - 1) // self.page_size
        
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_pages': total_pages,  
            'results': data
        })

class ListCompanyView(BaseCompanyView):
   
                                       
    pagination_class = CustomPagination

    
    def get(self, request):
     
        company = self.CompanyService.list_company()
        paginator = self.pagination_class()
        paginated_company = paginator.paginate_queryset(company, request)
        return paginator.get_paginated_response(CompanySerializer(paginated_company, many=True).data)



class ListCompanyNoPageView(BaseCompanyView):
    def get(self, request):
        companies = self.CompanyService.list_company()
        
         
        serialized_data = CompanySerializer(companies, many=True)
        
         
        return Response(serialized_data.data, status=200)

        
class CreateCompanyView(BaseCompanyView):
                                   

    def post(self, request):
        serializer = CompanyCreateUpdateSerializer(data=request.data)

        if serializer.is_valid():
                    try:
                         
                        validated_data = serializer.validated_data
                        name = validated_data['name']  
                        address = validated_data['address']       
                        email = validated_data['email']   

                         
                        company_data = self.CompanyService.create_company(name=name, address=address, email=email)

                         
                        serialized_company = CompanySerializer(company_data).data
                        return Response(serialized_company, status=status.HTTP_201_CREATED)
                    except Exception as e:
                        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateCompanyrView(BaseCompanyView):
    permission_classes = [IsAdmin]

    def put(self, request, company_id):
        serializer = CompanyCreateUpdateSerializer(data=request.data,partial=True)
        
        if serializer.is_valid():
        
            updated_company = self.CompanyService.update_company(company_id, serializer.validated_data)
            serialized_company = CompanySerializer(updated_company).data
            return Response(serialized_company, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteCompanyView(BaseCompanyView):
    permission_classes = [IsAdmin]

    def delete(self, request, company_id):
        
        self.CompanyService.delete_company(company_id)
        return Response(status=status.HTTP_200_OK)

class SearchCompanyView(BaseCompanyView):
    permission_classes = [IsAdmin]

    def get(self, request, company_id=None):
       
         
        if company_id:
            company = self.CompanyService.search_company(company_id)
              
            if company:
              
                company_serializer = CompanySerializer(company)
                return Response(company_serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "company not found."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"error": "company ID is required."}, status=status.HTTP_400_BAD_REQUEST)
    

class GetCompanyByEmailView(BaseCompanyView):
 

    def post(self, request):
        email = request.data.get("email")
          
  
        if email:
            company = self.CompanyService.get_company_by_email(email)
          
            if company:
                
                company_serializer = CompanySerializer(company)
                
                return Response(company_serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "company not found."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"error": "company email is required."}, status=status.HTTP_400_BAD_REQUEST)
    
class ToggleAutoPrioritizeView(BaseCompanyView):
    def post(self, request, company_id):
        try:
            company = self.CompanyService.toggle_auto_prioritize(company_id)
            return Response({"auto_prioritize": company.auto_prioritize}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class ToggleAutoCategorizeView(BaseCompanyView):
    def post(self, request, company_id):
        try:
            company = self.CompanyService.toggle_auto_categorize(company_id)
            return Response({"auto_categorize": company.auto_categorize}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)    

class ToggleAutoAssignView(BaseCompanyView):
    def post(self, request, company_id):
        try:
            company = self.CompanyService.toggle_auto_Assign(company_id)
            return Response({"auto_Assign": company.auto_assign}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)    
        
