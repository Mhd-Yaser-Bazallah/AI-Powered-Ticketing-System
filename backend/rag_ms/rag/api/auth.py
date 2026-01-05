from rest_framework.permissions import BasePermission
from django.conf import settings


class HasRagApiKey(BasePermission):
    header_name = "HTTP_X_RAG_API_KEY"

    def has_permission(self, request, view) -> bool:
        expected = getattr(settings, "RAG_API_KEY", "") or ""
        if not expected:
                                                              
            return False
        provided = request.META.get(self.header_name, "")
        return provided == expected
