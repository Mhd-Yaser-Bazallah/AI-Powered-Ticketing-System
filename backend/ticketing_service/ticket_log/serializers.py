from rest_framework import serializers
from .models import TicketLog

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketLog
        fields = ['ticket', 'user' , 'action' ,'previous_status', 'new_status', 'comments','created_at','company']

class LogCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketLog
        fields = [ 'ticket', 'user' , 'action' ,'previous_status', 'new_status', 'comments','company']
         
 