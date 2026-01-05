import uuid

from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser

from users_management.permissions import HasRagApiKey
from .models import UploadedFile
from .serializers import UploadFileSerializer, FileResponseSerializer
from .rag_client import build_file_payload, send_rag_task


class FileListCreateView(APIView):
                                         
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        company_id = request.query_params.get("company_id")
        if not company_id:
            return Response({"error": "company_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        files = UploadedFile.objects.filter(company_id=company_id)
        serializer = FileResponseSerializer(files, many=True)
        return Response({"items": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UploadFileSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = serializer.validated_data["file"]
        kind = serializer.validated_data["kind"]
        company = serializer.validated_data["company"]

        record = UploadedFile.objects.create(
            company=company,
            file=uploaded_file,
            original_name=uploaded_file.name,
            kind=kind,
            size_bytes=uploaded_file.size,
            content_type=getattr(uploaded_file, "content_type", "") or "",
        )

        payload = build_file_payload(record)
        transaction.on_commit(
            lambda: send_rag_task("rag.process_file_uploaded", payload)
        )

        response_serializer = FileResponseSerializer(record)
        return Response({"item": response_serializer.data}, status=status.HTTP_201_CREATED)


class FileDeleteView(APIView):
                                         

    def delete(self, request, file_id):
        record = get_object_or_404(UploadedFile, id=file_id)
        delete_payload = {
            "event": "file_deleted",
            "event_id": str(uuid.uuid4()),
            "file_id": str(record.id),
            "company_id": record.company_id,
        }
        if record.file:
            record.file.delete(save=False)
        record.delete()
        transaction.on_commit(
            lambda: send_rag_task("rag.process_file_deleted", delete_payload)
        )
        return Response({"deleted": True, "id": str(file_id)}, status=status.HTTP_200_OK)


                       
             
                                                                                                                              
             
                                                                             
              
                                                                                        
