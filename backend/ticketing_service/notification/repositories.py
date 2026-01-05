                              
from users_management.models import CustomUser
from .models import Notification

class NotificationRepository:
    def create_notification(self, recipient, ticket, message, company):
                          
        return Notification.objects.create(
            recipient=recipient,
            ticket=ticket,
            message=message,
            company=company
        )

    def get_user_notifications_by_id(self, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Notification.objects.none()                                        
        return Notification.objects.filter(recipient=user).order_by('-created_at')

    def mark_as_read(self, notification_id, user):
        notification = Notification.objects.filter(id=notification_id, recipient=user).first()
        if notification:
            notification.is_read = True
            notification.save()
        return notification

    def mark_all_as_read(self, user):
        Notification.objects.filter(recipient=user, is_read=False).update(is_read=True)
