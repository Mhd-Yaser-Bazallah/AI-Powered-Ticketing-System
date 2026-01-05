from django.apps import AppConfig



class UsersManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users_management'



    def ready(self):
        from injector import Injector
        from .injector_config import configure
        injector = Injector([configure])
        self.injector = injector