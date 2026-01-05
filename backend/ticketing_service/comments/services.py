from injector import inject
from .repositories import CommentRepository
from rest_framework.exceptions import NotFound
from .models import Comments  
from users_management.repositories import UserRepository
from rest_framework.response import Response
from rest_framework import status
class CommentService:
    @inject
    def __init__(self, Comment_repo: CommentRepository,user_repo:UserRepository):
        self.Comment_repo = Comment_repo
        self.user_repo = user_repo

    def list_comments(self):
        return self.Comment_repo.get_all_comments()

    def create_comments(self, ticket, user, description):
        try: 
            return self.Comment_repo.create_comment(ticket, user, description)
        except Exception as e:
            raise e

    def comments_by_userID(self,user_id):
        try:
            comment = self.Comment_repo.get_comments_by_user_id(user_id)
        except Comments.DoesNotExist:
            raise NotFound("Comment not found")    
        return comment
    
    def comments_by_ticket_id(self,ticket_id):
        try:
            comment = self.Comment_repo.get_comments_by_ticket_id(ticket_id)
        except Comments.DoesNotExist:
            raise NotFound("Comment not found")    
        return comment
    
    def update_comment(self, Comment_id, validated_data):
        try: 
            comment = self.Comment_repo.get_comment_by_id(Comment_id)
             
        except Comments.DoesNotExist:
            raise NotFound("Comments not found")
        return self.Comment_repo.update_comment(comment, validated_data)

    def delete_comment(self, Comment_id):
        try:
            comment = self.Comment_repo.get_comment_by_id(Comment_id)
        except Comments.DoesNotExist:
            raise NotFound("Comment not found")
        self.Comment_repo.delete_comment(comment)    

    def search_comment(self, Comment_id):
        try:
             comment= self.Comment_repo.get_comment_by_id(Comment_id)
        except Comments.DoesNotExist:
            raise NotFound("Comments not found")
        return comment
   