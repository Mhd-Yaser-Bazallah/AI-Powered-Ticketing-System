from injector import inject
from .repositories import UserRepository
from rest_framework.exceptions import NotFound
from .models import CustomUser
class UserService:
    @inject
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def list_users(self):
        return self.user_repo.get_all_users()

    def create_user(self, validated_data):
 
        try:
            return self.user_repo.create_support_team_manager(validated_data)
        except Exception as e:
 
            raise e


    def create_Team_member(self, validated_data):
         
            try:
                return self.user_repo.create_support_team_member(validated_data)
            except Exception as e:
        
                raise e
        
    def update_user(self, user_id, validated_data):
        try:
            user = self.user_repo.get_user_by_id(user_id)
        except CustomUser.DoesNotExist:
            raise NotFound("User not found")
        return self.user_repo.update_user(user, validated_data)

    def delete_user(self, user_id):
        try:
            user = self.user_repo.get_user_by_id(user_id)
        except CustomUser.DoesNotExist:
            raise NotFound("User not found")
        self.user_repo.delete_user(user)

    def search_users(self, user_id):
        return self.user_repo.get_user_by_id(user_id)

    def update_account(self, user_id, validated_data):
        try:
            user = self.user_repo.get_user_by_id(user_id)
        except CustomUser.DoesNotExist:
            raise NotFound("User not found")
        return self.user_repo.update_user(user, validated_data)

    def delete_account(self, user_id):
        try:
            user = self.user_repo.get_user_by_id(user_id)
        except CustomUser.DoesNotExist:
            raise NotFound("User not found")
        self.user_repo.delete_user(user)
