from django.shortcuts import render
from injector import inject 
from rest_framework.views import APIView

from notification.repositories import NotificationRepository
from notification.services import NotificationService
from users_management.repositories import UserRepository
                         
from .services import CommentService
from .repositories import CommentRepository
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from users_management.permissions import CommentCRUD, IsUser
from .serializers import CommentsCreateUpdateSerializer , CommentSerializer

class BaseCommentView(APIView):
    @inject
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.CommentService = CommentService(CommentRepository(), UserRepository())
        self.notification_service = NotificationService(NotificationRepository())


class ListCommentView(BaseCommentView): 
    def get(self, request):
       
        comments = self.CommentService.list_comments()
        serialized_data = CommentSerializer(comments, many=True)
        return Response(serialized_data.data, status=200)

class CreateCommentView(BaseCommentView):
    permission_classes = [CommentCRUD]

    def post(self, request):
        serializer = CommentsCreateUpdateSerializer(data=request.data)
 
        if serializer.is_valid():
                    
                    try:
                        validated_data = serializer.validated_data
                        ticket = validated_data['ticket']  
                        user = validated_data['user']       
                        description = validated_data['description']   
                        
                        
                        comment_data = self.CommentService.create_comments(ticket , user, description)

                        
                        serialized_comment = CommentSerializer(comment_data).data
                        self.notification_service.notify_user(user, ticket, f"The ticket: {ticket.id}has been commented on.", "")
                        return Response(serialized_comment, status=status.HTTP_201_CREATED)
                    except Exception as e:
                        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateCommentrView(BaseCommentView):
    permission_classes = [CommentCRUD]

    def put(self, request, comment_id):
        serializer = CommentsCreateUpdateSerializer(data=request.data,partial=True)
        
        if serializer.is_valid():
             
            updated_comment = self.CommentService.update_comment(comment_id, serializer.validated_data)
            serialized_user = CommentSerializer(updated_comment).data
            return Response(serialized_user, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteCommentView(BaseCommentView):
    permission_classes = [CommentCRUD]

    def delete(self, request, comment_id):
        self.CommentService.delete_comment(comment_id)
        return Response(status=status.HTTP_200_OK)

class CommentByUserIDView(BaseCommentView):
    permission_classes = [IsUser]
     
    def get(self,request,user_id):
   
        comments = self.CommentService.comments_by_userID(user_id)
        paginator = self.pagination_class()
        if comments:
                 
            serialized_data = CommentSerializer(comments, many=True)
            return Response(serialized_data.data, status=200)
        return Response({"error": "user dont have any comment."}, status=status.HTTP_404_NOT_FOUND)   
              
class CommentByTicketIDView(BaseCommentView):
   
    def get(self,request,ticket_id):
         
        comments = self.CommentService.comments_by_ticket_id(ticket_id)
       
         
        serialized_data = CommentSerializer(comments, many=True)
        return Response(serialized_data.data, status=200)  
 

class SearchCommentView(BaseCommentView):
    permission_classes = [CommentCRUD]

    def get(self, request, comment_id=None):
 
        if comment_id:
            comment = self.CommentService.search_comment(comment_id)
 
            if comment:
 
                comment_serializer = CommentSerializer(comment)
                return Response(comment_serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"error": "Comment ID is required."}, status=status.HTTP_400_BAD_REQUEST)
