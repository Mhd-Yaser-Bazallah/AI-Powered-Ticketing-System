from datetime import timezone
from typing import List, Optional

from injector import inject
from .models import CustomUser 
from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password

class UserRepository:
    @inject
    def create_user(self, email: str, username: str, password: str, **extra_fields) -> CustomUser:
        if not email:
            raise ValueError("Email is required")

        hashed_password = make_password(password)
        extra_fields['password'] = hashed_password

        user = CustomUser(email=email, username=username, **extra_fields)
        user.save()
        return user

    def get_all_users(self) -> QuerySet:
        return CustomUser.objects.all()

    def get_user_by_id(self, user_id) -> CustomUser:
            return CustomUser.objects.get(id=user_id)
         
        
    def get_by_email(self, user_email: str) -> CustomUser:
        try:
            return CustomUser.objects.get(email=user_email)
        except CustomUser.DoesNotExist:
            raise ObjectDoesNotExist("User not found.")   

  
    def create_client_user(self, data: dict) -> CustomUser:
        data['role'] = 'client'
        try:
            user = self.create_user(**data)
   
            return user
        except Exception as e:
             raise e
        

    def create_support_team_manager(self, data: dict) -> CustomUser:
     
        data['role'] = 'support_team_manager'
        try:
            user = self.create_user(**data)
    
            return user
        except Exception as e:
 
            raise e

    def create_support_team_member(self, data: dict) -> CustomUser:
        data['role'] = 'support_team_member'
        user = self.create_user(**data)
        user.save()
        return user
    
    def update_user(self, user: CustomUser, updated_data: dict) -> CustomUser:
        for attr, value in updated_data.items():
            setattr(user, attr, value)
        user.save()
        return user

    def delete_user(self, user: CustomUser) -> None:
        user.delete()

    def filter_users(self, **filters) -> QuerySet:
        return CustomUser.objects.filter(**filters)


    def get_team_members_by_company(company)-> CustomUser :

     team_members = CustomUser.objects.filter(company_id=company, role="support_team_member").order_by('id')
     return team_members
