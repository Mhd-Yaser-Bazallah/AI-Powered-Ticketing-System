                          
from django.urls import path
from . import views

urlpatterns = [ 
    path('List', views.ListCommentView.as_view(), name='comment-list'),           
    path('create', views.CreateCommentView.as_view(), name='user-create'),      
    path('update/<int:comment_id>', views.UpdateCommentrView.as_view(), name='user-update'),  
    path('delete/<int:comment_id>', views.DeleteCommentView.as_view(), name='user-delete'),   
    path('search/<int:comment_id>', views.SearchCommentView.as_view(), name='comment-search'), 
    path('commentsUser/<int:user_id>', views.CommentByUserIDView.as_view(), name='comment-by-userId'),
    path('commentsTicket/<int:ticket_id>', views.CommentByTicketIDView.as_view(), name='comment-by-ticket_id'),
    ]
