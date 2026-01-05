from injector import inject 
from rest_framework.views import APIView

                         
from .services import TicketLogService
from .repositories import ticketLogRepository
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from users_management.permissions import IsUser 
from .serializers import LogCreateUpdateSerializer ,LogSerializer

class BaseLogView(APIView):
    @inject
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.TicketLogService = TicketLogService(ticketLogRepository())

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

class ListLogView(BaseLogView):
 
    permission_classes = [IsUser] 
    pagination_class = CustomPagination
 
    def get(self, request):
  
        log = self.TicketLogService.list_log()
        paginator = self.pagination_class()
        paginated_log = paginator.paginate_queryset(log, request)
        return paginator.get_paginated_response(LogSerializer(paginated_log, many=True).data)


class ListLogCompanyView(BaseLogView):
 
    permission_classes = [IsUser] 
    pagination_class = CustomPagination

 
    def get(self, request,company_id):
  
        log = self.TicketLogService.list_log_company(company_id)
        paginator = self.pagination_class()
        paginated_log = paginator.paginate_queryset(log, request)
        return paginator.get_paginated_response(LogSerializer(paginated_log, many=True).data)

class CreateLogView(BaseLogView):
 
    def post(self, request):
   
        serializer = LogCreateUpdateSerializer(data=request.data)
         
        if serializer.is_valid():
                    try:  
                        validated_data = serializer.validated_data
                  
                        comments = validated_data['comments']  
                        ticket = validated_data['ticket']       
                        user = validated_data['user']   
                        action = validated_data['action'] 
                        previous_status = validated_data['previous_status'] 
                        new_status = validated_data['new_status'] 
                        company=validated_data['company'] 
                        log_data = self.TicketLogService.create_log(comments=comments, ticket=ticket, user=user,
                                                                    action=action,previous_status=previous_status,
                                                                    new_status=new_status,company=company)
 
                     
                        serialized_log = LogSerializer(log_data).data
                         
                        return Response(serialized_log, status=status.HTTP_201_CREATED)
                    except Exception as e:
                        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchLogView(BaseLogView):
    permission_classes = [IsUser]

    def get(self, request, log_id=None):
 
        if log_id:
            log = self.TicketLogService.search_log(log_id)
            if log:
                log_serializer =LogSerializer(log)
                return Response(log_serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "log not found."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"error": "log  ID is required."}, status=status.HTTP_400_BAD_REQUEST)
    
 