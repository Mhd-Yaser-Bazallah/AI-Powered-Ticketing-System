                     
from rest_framework import serializers
from users_management.models import CustomUser
from django.contrib.auth.hashers import make_password
from .jwt_utils import get_tokens_for_user

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'company_id', 'phone_number','password')  

        extra_kwargs = {'password': {'write_only': True} 
                        }
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()
