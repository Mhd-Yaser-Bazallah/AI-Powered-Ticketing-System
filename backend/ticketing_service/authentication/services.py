from rest_framework.exceptions import AuthenticationFailed
from authentication.jwt_utils import get_tokens_for_user
from django.contrib.auth.hashers import check_password
from users_management.repositories import UserRepository  
from django.core.exceptions import ObjectDoesNotExist

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository  
    def register_user(self, serializer):
         
        user = self.user_repository.create_client_user(serializer.validated_data)

        token = get_tokens_for_user(user)
        return {'token': token}
        
    def login_user(self, email, password):
        try:
          
            user = self.user_repository.get_by_email(email)
            
        except ObjectDoesNotExist:
            raise AuthenticationFailed('Invalid email or password')
 
        if not check_password(password, user.password):
            raise AuthenticationFailed('Invalid email or password')

         
        token = get_tokens_for_user(user)
        return {'token': token}
