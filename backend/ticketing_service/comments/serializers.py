from rest_framework import serializers
from .models import Comments
from users_management.models import CustomUser



class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ['id','ticket', 'user','username','description','created_at']
    def get_username(self, comment):
        
        user = CustomUser.objects.filter(id=comment.user.id).first()
        if user:
            return user.username   
        return None   

 

class CommentsCreateUpdateSerializer(serializers.ModelSerializer):
    ticket = serializers.IntegerField()
    user =serializers.IntegerField()
    class Meta:
        model = Comments    
        fields = ['ticket', 'user','description']
         
 

 