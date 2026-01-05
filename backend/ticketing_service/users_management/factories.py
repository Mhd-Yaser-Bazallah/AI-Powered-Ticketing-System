from abc import ABC, abstractmethod
from .services import UserService
from .repositories import UserRepository

class AbstractServiceFactory(ABC):
    @abstractmethod
    def create_user_service(self):
        pass

class ServiceFactory(AbstractServiceFactory):
    def create_user_service(self):
        user_repo = UserRepository()
        return UserService(user_repo)
