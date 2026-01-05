from rest_framework import serializers

class AnalysisSerializer(serializers.Serializer):
    total_tickets = serializers.IntegerField()
    tickets_by_status = serializers.ListField()
    assigned_vs_unassigned = serializers.DictField()
    tickets_by_team = serializers.ListField()
    tickets_by_user = serializers.ListField()
