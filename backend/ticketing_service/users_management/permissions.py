import jwt
                                       
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import os
from dotenv import load_dotenv

                                           
load_dotenv()

class BaseRolePermission():
    required_roles = []

    def has_permission(self, request, view):
 
        cookie_header = request.headers.get('Authorization') 
         
        if not cookie_header :
            raise AuthenticationFailed("you are not loged in")

                                                  
        token = cookie_header.split('=')[1]   
        
        try:
            if not token :  
                 raise AuthenticationFailed("you are not loged in")
 
        except IndexError:
            raise AuthenticationFailed("Invalid token format")

         
      
       
        try:  
            payload = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])                    
        
            user_role = payload.get('role')                               
         
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed (f'Invalid token: {str(e)}')
        

        return user_role in self.required_roles

class IsUser(BaseRolePermission):
    def __init__(self):
         self.required_roles = ['client','support_team_member','support_team_manager','admin']
            
class IsAdmin(BaseRolePermission):
    def __init__(self):
         self.required_roles = ['admin']


class IsSupportTeamMember(BaseRolePermission):
    def __init__(self):
        self.required_roles = ['support_team_member']


class IsSupportTeamManager(BaseRolePermission):
   def __init__(self):
        self.required_roles = ['support_team_manager','admin']


class IsSupportStaff(BaseRolePermission):
    def __init__(self):
        self.required_roles = ['support_team_member', 'support_team_manager']


class IsClient(BaseRolePermission):
    def __init__(self):
        self.required_roles = ['client']

class CommentCRUD(BaseRolePermission):
    def __init__(self):
        self.required_roles = ['support_team_member','support_team_manager','client','admin']


class HasRagApiKey():
    def has_permission(self, request, view):
        api_key = request.headers.get('X-RAG-API-KEY')
        if not api_key:
            raise AuthenticationFailed("X-RAG-API-KEY header is required")

        expected_key = getattr(settings, "RAG_API_KEY", "")
        if not expected_key or api_key != expected_key:
            raise AuthenticationFailed("Invalid RAG API key")

        return True

