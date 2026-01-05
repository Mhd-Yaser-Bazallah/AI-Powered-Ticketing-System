import logging

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ticket.models import AnalyzeCounter, Company
from ticket.tasks import export_tickets_and_retrain
from ticket.utils.Categorize import TicketClassifier
from ticket.utils.prioritize import determine_ticket_priority
from ticket.utils.ml.inference.ticket_router import router


class TicketAnalyzeRequestSerializer(serializers.Serializer):
    description = serializers.CharField()
    company_id = serializers.IntegerField()


classifier = TicketClassifier()
logger = logging.getLogger(__name__)


class TicketAnalyzeView(APIView):
    def post(self, request):
        serializer = TicketAnalyzeRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        description = serializer.validated_data["description"]
        company_id = serializer.validated_data["company_id"]

        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)

        category = classifier.predict(description)
        priority = determine_ticket_priority(description)
        routing = router.route_ticket(company, description)

        triggered_training = False
        with transaction.atomic():
            counter, _ = AnalyzeCounter.objects.select_for_update().get_or_create(pk=1)
            counter.count += 1
            logger.info("Analyze counter incremented to %s", counter.count)

            if (
                counter.count >= settings.ANALYZE_TRAINING_THRESHOLD
                and not counter.is_training
            ):
                counter.count = 0
                counter.is_training = True
                counter.last_triggered_at = timezone.now()
                counter.last_error = None
                triggered_training = True
                counter.save(
                    update_fields=[
                        "count",
                        "is_training",
                        "last_triggered_at",
                        "last_error",
                        "updated_at",
                    ]
                )
            else:
                counter.save(update_fields=["count", "updated_at"])

        if triggered_training:
            try:
                export_tickets_and_retrain.delay()
                logger.info("Analyze threshold reached; training enqueued.")
            except Exception as exc:
                logger.exception("Failed to enqueue training task: %s", exc)
                with transaction.atomic():
                    counter, _ = AnalyzeCounter.objects.select_for_update().get_or_create(pk=1)
                    counter.is_training = False
                    counter.last_error = str(exc)
                    counter.save(update_fields=["is_training", "last_error", "updated_at"])

        return Response(
            {
                "category": category,
                "priority": priority,
                "team_assignment": routing,
            },
            status=status.HTTP_200_OK,
        )
