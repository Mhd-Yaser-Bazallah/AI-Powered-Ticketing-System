import os

from django.utils import timezone
from rest_framework import serializers

from company.models import Company
from .models import UploadedFile


class UploadFileSerializer(serializers.Serializer):
    file = serializers.FileField()
    kind = serializers.ChoiceField(choices=UploadedFile.KIND_CHOICES)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())

    def validate(self, attrs):
        uploaded_file = attrs.get("file")
        kind = attrs.get("kind")

        extension = os.path.splitext(uploaded_file.name)[1].lower()
        allowed_extensions = {
            UploadedFile.KIND_PDF: [".pdf"],
            UploadedFile.KIND_WORD: [".doc", ".docx"],
            UploadedFile.KIND_EXCEL: [".xls", ".xlsx"],
        }

        if extension not in allowed_extensions[kind]:
            allowed_list = ", ".join(allowed_extensions[kind])
            raise serializers.ValidationError(
                {"file": f"Invalid file extension for {kind}. Allowed: {allowed_list}"}
            )

        return attrs


class FileResponseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="original_name")
    sizeBytes = serializers.IntegerField(source="size_bytes")
    companyId = serializers.IntegerField(source="company_id")
    uploadedAt = serializers.SerializerMethodField()

    class Meta:
        model = UploadedFile
        fields = ["id", "name", "kind", "sizeBytes", "companyId", "uploadedAt"]
        
    def get_uploadedAt(self, obj):
        dt = obj.uploaded_at
        if not dt:
            return None

                                       
        if timezone.is_naive(dt):
            return int(dt.timestamp() * 1000)

                                    
        return int(timezone.localtime(dt).timestamp() * 1000)
