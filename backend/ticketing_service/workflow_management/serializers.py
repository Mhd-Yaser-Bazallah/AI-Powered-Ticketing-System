from rest_framework import serializers

from users_management.models import CustomUser
from .models import Workflow, WorkflowStep

class WorkflowStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowStep
        fields = ['id', 'name', 'order']

class WorkflowSerializer(serializers.ModelSerializer):
    steps = WorkflowStepSerializer(many=True)
    created_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Workflow
        fields = ['id', 'name', 'company', 'created_by', 'created_at', 'steps']

    def create(self, validated_data):
        steps_data = validated_data.pop('steps')
        workflow = Workflow.objects.create(**validated_data)
        for index, step_data in enumerate(steps_data):
            WorkflowStep.objects.create(workflow=workflow, name=step_data['name'], order=index)
        return workflow