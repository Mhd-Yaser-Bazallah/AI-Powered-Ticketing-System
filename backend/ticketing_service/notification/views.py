                       
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from injector import inject

from notification.repositories import NotificationRepository
from users_management.models import CustomUser
from .services import NotificationService
from .serializers import NotificationSerializer

class BaseNotificationView(APIView):
    @inject
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.notification_service = NotificationService(NotificationRepository())


class NotificationListView(BaseNotificationView):
    def get(self,request,user_id):
                                                                                   
        if not user_id:
            return Response({"error": "User ID is required"}, status=400)
        
        notifications = self.notification_service.get_user_notifications_by_id(user_id)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=200)
    

class MarkAsReadView(BaseNotificationView):
    def post(self, request, notification_id):
        user_id = request.data.get("user")
        if not user_id:
            return Response({"error": "User ID is required"}, status=400)

                                
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        notif = self.notification_service.mark_as_read(notification_id, user)
        if notif:
            return Response({"message": "Marked as read"}, status=200)
        return Response({"error": "Notification not found"}, status=404)


class MarkAllAsReadView(BaseNotificationView):
    def post(self, request):
        user_id = request.data.get("user")
        if not user_id:
            return Response({"error": "User ID is required"}, status=400)

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        self.notification_service.mark_all_as_read(user)
        return Response({"message": "All notifications marked as read"}, status=200)
