from rest_framework import serializers

from team.models import Team
from .models import CustomUser, Membership
from authentication.jwt_utils import get_tokens_for_user
from company.models import Company
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['id', 'active','email', 'username', 'company_id','phone_number', 'role', 'created_at']
    
    
class UserCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username','company_id','phone_number', 'role', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [ 'email','username', 'company_id', 'phone_number', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

class UserSearchSerializer(serializers.ModelSerializer):
    team_id = serializers.SerializerMethodField()
    company= serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'role','created_at','phone_number','company_id','company','team_id']
    
    def get_team_id(self, user): 
        membership = Membership.objects.filter(user_id=user.id).first()
        if membership:
            return membership.team_id.id   
        return None
    
    def get_company(self, user):
         
        if user.company_id:
            return user.company_id.name   
        return None    
    
class TeamMemberSerializer(serializers.ModelSerializer):
    team_name = serializers.SerializerMethodField()  
    team_id = serializers.SerializerMethodField()  
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'company_id', 'phone_number', 'role', 'created_at', 'active', 'team_name','team_id']                      

    def get_team_name(self, user):
         
        membership = Membership.objects.filter(user_id=user.id).first()
        if membership:
            team = Team.objects.get(id=membership.team_id.id)   
            return team.category   
        return None
    
    def get_team_id(self, user):
 
        membership = Membership.objects.filter(user_id=user.id).first()
        if membership:
            return membership.team_id.id 
        return None