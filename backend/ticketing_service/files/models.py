import uuid

from django.db import models

from company.models import Company


class UploadedFile(models.Model):
    KIND_PDF = "pdf"
    KIND_WORD = "word"
    KIND_EXCEL = "excel"

    KIND_CHOICES = (
        (KIND_PDF, "PDF"),
        (KIND_WORD, "Word"),
        (KIND_EXCEL, "Excel"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    file = models.FileField(upload_to="files/")
    original_name = models.CharField(max_length=255)
    kind = models.CharField(max_length=10, choices=KIND_CHOICES)
    size_bytes = models.BigIntegerField()
    content_type = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "UploadedFile"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.original_name} ({self.kind})"
