 
from injector import inject
from .models import Comments  
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from django.db.models import QuerySet

class CommentRepository:
    @inject

    def create_comment(self, ticket, user, description) -> Comments:
 
        comment = Comments(ticket_id=ticket, user_id=user, description=description)
        comment.save()
        return comment
    
    def get_comments_by_user_id(self,user_id: int)-> QuerySet:
        return Comments.objects.filter(user_id = user_id).order_by('created_at')
    
    def get_comments_by_ticket_id(self,ticket_id)-> QuerySet:
        return Comments.objects.filter(ticket_id = ticket_id).order_by('created_at')

    def get_all_comments(self) -> QuerySet:
        return Comments.objects.all().order_by('created_at')
    
    def get_comment_by_id(self, comments_id: int) -> Comments:
        return Comments.objects.get(id=comments_id)
         
        
    def update_comment(self, Comment: Comments, updated_data: dict) -> Comments:
        for attr, value in updated_data.items():
            setattr(Comment, attr, value)
        Comment.save()
        return Comment

    def delete_comment(self, Comment: Comments) -> None:
        Comment.delete()   
   
