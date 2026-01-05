                          
from injector import inject

from notification.models import Notification
from .repositories import NotificationRepository
from users_management.models import Membership

class NotificationService:
    @inject
    def __init__(self, notification_repo: NotificationRepository):
        self.notification_repo = notification_repo

    def notify_user(self, user, ticket, message, company):
        self.notification_repo.create_notification(user, ticket, message, company)

    def notify_team(self, team, ticket, message, company):
        memberships = Membership.objects.filter(team_id=team)
        for m in memberships:
            self.notify_user(m.user_id, ticket, message, company)

    def get_user_notifications_by_id(self, user):
        return self.notification_repo.get_user_notifications_by_id(user)

    def mark_as_read(self, notification_id, user):
        return self.notification_repo.mark_as_read(notification_id, user)
    
    def mark_all_as_read(self, user):
        Notification.objects.filter(recipient=user, is_read=False).update(is_read=True)
