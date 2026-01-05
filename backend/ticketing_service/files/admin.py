from django.contrib import admin

from .models import UploadedFile


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ("id", "original_name", "kind", "size_bytes", "uploaded_at")
    search_fields = ("original_name", "kind")
