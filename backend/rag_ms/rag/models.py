from django.db import models
import uuid


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

                                                                                    
    ticket_description = models.TextField(null=True, blank=True)
    ticket_category = models.CharField(max_length=100, null=True, blank=True)
    ticket_priority = models.CharField(max_length=50, null=True, blank=True)

                                                                      
    summary = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Conversation {self.id}"


class Message(models.Model):
    ROLE_USER = "user"
    ROLE_ASSISTANT = "assistant"
    ROLE_CHOICES = [
        (ROLE_USER, "User"),
        (ROLE_ASSISTANT, "Assistant"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.role} @ {self.created_at}"


class Ticket(models.Model):
    id = models.IntegerField(primary_key=True)
    solution_steps = models.JSONField(null=True, blank=True)
    solution_confidence = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "Ticket"
        managed = False


class ProcessedEvent(models.Model):
    STATUS_PROCESSING = "processing"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = [
        (STATUS_PROCESSING, "processing"),
        (STATUS_COMPLETED, "completed"),
        (STATUS_FAILED, "failed"),
    ]

    event_id = models.CharField(max_length=64, unique=True)
    event_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PROCESSING)
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
