from rest_framework import serializers

from company.models import Company
from users_management.models import CustomUser
from .models import Ticket, Ticket_Team_Assignment

class TicketSerializer(serializers.ModelSerializer):
    team_name = serializers.SerializerMethodField()
    class Meta:
        model = Ticket
        fields = [
            'id',
            'client',
            'team_name',
            'company',
            'category',
            'priority',
            'description',
            'title',
            'status',
            'created_at',
            'solution_steps',
            'human_solution_steps',
            'human_solved_at',
            'human_solved_by',
        ]
        

    def get_team_name(self, ticket):
         
        assignment = Ticket_Team_Assignment.objects.filter(Ticket=ticket).first()
        if assignment:
            return assignment.Team.category   
        return None
        
class TicketCreateUpdateSerializer(serializers.ModelSerializer):
    client = serializers.IntegerField()
    company = serializers.IntegerField()

    class Meta:
        model = Ticket
        fields = ['id','description','title','client','company','status' ,'priority','category']


class SolveTicketSerializer(serializers.Serializer):
    steps = serializers.ListField()
    comment = serializers.CharField(required=False, allow_blank=True, max_length=500)
    user_id = serializers.IntegerField(required=False)

    def validate_steps(self, value):
        if not isinstance(value, list) or not value:
            raise serializers.ValidationError("steps must be a non-empty list")

        normalized = []
        for idx, item in enumerate(value):
            if isinstance(item, str):
                text = item.strip()
            elif isinstance(item, dict):
                text = str(item.get("text", "")).strip()
            else:
                raise serializers.ValidationError("steps items must be string or object")

            if not text:
                raise serializers.ValidationError("steps items must not be empty")

            normalized.append({"order": idx + 1, "text": text})

        if len(normalized) > 50:
            raise serializers.ValidationError("too many steps (max 50)")

        return normalized
         
 
 
