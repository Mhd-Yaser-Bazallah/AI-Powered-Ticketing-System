from injector import inject
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    UserSerializer, UserCreateUpdateSerializer, AccountUpdateSerializer, UserSearchSerializer
)
from rest_framework.pagination import PageNumberPagination
from .permissions import IsAdmin ,IsUser
from .factories import ServiceFactory
from rest_framework.exceptions import NotFound, PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
import os
from dotenv import load_dotenv
import jwt
load_dotenv()

class BaseUserView(APIView):
    @inject
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service_factory = ServiceFactory()
        self.user_service = self.service_factory.create_user_service()


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

class ListUsersView(BaseUserView):
      
    pagination_class = CustomPagination

    def get(self, request):
        users = self.user_service.list_users()
        paginator = self.pagination_class()
        paginated_users = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(UserSerializer(paginated_users, many=True).data)

class CreateUserView(BaseUserView):
    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = UserCreateUpdateSerializer(data=request.data)
 
        
        if serializer.is_valid():
 
            try:
                user_data = self.user_service.create_user(serializer.validated_data)
                serialized_user = UserSerializer(user_data).data
                return Response(serialized_user, status=status.HTTP_201_CREATED)
            except Exception as e:
  
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
   
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateUserView(BaseUserView):
                                    

    def put(self, request, user_id):
        serializer = UserCreateUpdateSerializer(data=request.data,partial=True)
       
        if serializer.is_valid():
            updated_user = self.user_service.update_user(user_id, serializer.validated_data)
            serialized_user = UserSerializer(updated_user).data
            return Response(serialized_user, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteUserView(BaseUserView):
    permission_classes = [IsAdmin]

    def delete(self, request, user_id):
        self.user_service.delete_user(user_id)
        return Response({"error": "user deleted successfully"},status=status.HTTP_200_OK)
         
class SearchUserView(BaseUserView):
    permission_classes = [IsAdmin]

    def get(self, request, user_id=None):
        
        if user_id:
            user = self.user_service.search_users(user_id)
            if user:
                user_serializer = UserSearchSerializer(user)
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)


class getMeView(BaseUserView):
                                   

    def get(self, request, user_id=None): 
        if user_id:
            
            user = self.user_service.search_users(user_id)
            if user:
                
                user_serializer = UserSearchSerializer(user)
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)




class AccountUpdateView(BaseUserView):
    permission_classes = [IsUser]
 
    def put(self, request, *args, **kwargs): 
        cookie_header = request.headers.get('Authorization') 
        token = cookie_header.split('=')[1]
        try: 
            payload = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
            user_id = payload.get('user_id') 
            if not user_id:
                return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
            
            if 'role' in request.data:
                return Response({"error": "You cannot change your role."}, status=status.HTTP_403_FORBIDDEN)
 
            serializer = AccountUpdateSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                try: 
                    updated_user = self.user_service.update_account(user_id, serializer.validated_data)
                    return Response(AccountUpdateSerializer(updated_user).data, status=status.HTTP_200_OK)
                except ObjectDoesNotExist as e:
                    return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except jwt.ExpiredSignatureError:
            return Response({"error": "Token has expired."}, status=status.HTTP_401_UNAUTHORIZED)
       
        


    def delete(self, request): 
        cookie_header = request.headers.get('Authorization') 
        token = cookie_header.split('=')[1]
        if not token:
            return Response({"error": "Authentication token not provided."}, status=status.HTTP_403_FORBIDDEN)

        try: 
            payload = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
            user_id = payload.get('user_id')

            if not user_id:
                return Response({"error": "Invalid token."}, status=status.HTTP_403_FORBIDDEN)
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token has expired."}, status=status.HTTP_403_FORBIDDEN)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token."}, status=status.HTTP_403_FORBIDDEN)
          
          
        try:
            self.user_service.delete_account(user_id)
            response=Response({"detail": "Account deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
            response.delete_cookie('jwt')
            return response
        except NotFound as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
