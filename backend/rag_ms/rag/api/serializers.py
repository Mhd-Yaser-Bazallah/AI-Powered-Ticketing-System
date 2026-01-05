from rest_framework import serializers


class TicketContextSerializer(serializers.Serializer):
    description = serializers.CharField(required=True, allow_blank=False)
    category = serializers.CharField(required=False, allow_blank=True)
    priority = serializers.CharField(required=False, allow_blank=True)


class SolutionRequestSerializer(serializers.Serializer):
    ticket_description = serializers.CharField(required=True, allow_blank=False)
    context = serializers.DictField(required=False)
    company_id = serializers.IntegerField(required=True)


class SolutionResponseSerializer(serializers.Serializer):
    mode = serializers.CharField()
    steps = serializers.ListField(child=serializers.CharField())
    confidence = serializers.FloatField()
    sources = serializers.ListField(child=serializers.DictField())
    needs_human = serializers.BooleanField()


class ChatRequestSerializer(serializers.Serializer):
    conversation_id = serializers.UUIDField(required=False, allow_null=True)
    message = serializers.CharField(required=True, allow_blank=False)
    company_id = serializers.IntegerField(required=True)

                                                                   
    ticket = TicketContextSerializer(required=False)


class ChatResponseSerializer(serializers.Serializer):
    mode = serializers.CharField()
    conversation_id = serializers.UUIDField()
    answer = serializers.CharField(allow_blank=True)
    confidence = serializers.FloatField()
    sources = serializers.ListField(child=serializers.DictField())
    refusal = serializers.CharField(allow_null=True)
    classification = serializers.CharField(required=False)
    refusal_code = serializers.CharField(allow_null=True, required=False)
    needs_human = serializers.BooleanField(required=False)


class RetrieveRequestSerializer(serializers.Serializer):
    query = serializers.CharField(required=True, allow_blank=False)
    company_id = serializers.IntegerField(required=True)
    top_k = serializers.IntegerField(required=False, min_value=1, max_value=50, default=5)
    filters = serializers.DictField(required=False)
    score_threshold = serializers.FloatField(required=False, allow_null=True)

class RetrieveResponseSerializer(serializers.Serializer):
    items = serializers.ListField(child=serializers.DictField())


class SeedRequestSerializer(serializers.Serializer):
    wipe = serializers.BooleanField(required=False, default=False)
    company_id = serializers.IntegerField(required=False, default=0)


 
