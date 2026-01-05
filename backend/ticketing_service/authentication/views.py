from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
from .services import AuthService
from users_management.repositories import UserRepository
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class BaseAuthView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_service = AuthService(UserRepository())   

class RegisterView(BaseAuthView):
    def post(self, request):

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
 
                token_data = self.auth_service.register_user(serializer)

                response = Response(token_data, status=status.HTTP_201_CREATED)
                               
                response.set_cookie(
                    key='jwt',
                    value=token_data['token'],
                    httponly=True,
                    secure=False,
                    samesite='Lax',
                    max_age=3600
                )
                return response
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(BaseAuthView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():

            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
           
            try:
                 
                token_data = self.auth_service.login_user(email, password)
                response = Response(token_data, status=status.HTTP_200_OK)
                response.set_cookie(
                    key='jwt',
                    value=token_data['token'],
                    httponly=True,
                    secure=False,
                    samesite='Lax',
                    max_age=3600,   
                     
                )
                return response
            except AuthenticationFailed as e:
                return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
            
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

class LogoutView(BaseAuthView):

    def post(self, request):
 
        response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
  
        return response
