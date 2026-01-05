from rest_framework import serializers
from .models import Team

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id','company','category', 'description','created_at']


class ListMemmberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'active','email', 'username', 'company_id','phone_number', 'role', 'created_at','team']

class TeamCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['description','category','company']
         
 