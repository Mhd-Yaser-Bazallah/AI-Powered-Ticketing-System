from injector import Binder
from .repositories import UserRepository
from .services import UserService
from comments.repositories import CommentRepository
from comments.services import CommentService

def configure(binder: Binder):
    binder.bind(UserRepository, to=UserRepository)
    binder.bind(UserService, to=UserService)
    binder.bind(CommentRepository, to=CommentRepository)
    binder.bind(CommentService, to=CommentService)