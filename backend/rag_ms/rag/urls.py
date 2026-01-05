from django.urls import path
from rag.api.views import HealthView, RagChatView, RagSolutionView
from rag.api.views import DevSeedView, RagRetrieveView, RagEventView

urlpatterns = [
    path("health", HealthView.as_view(), name="health"),
    path("chat", RagChatView.as_view(), name="rag-chat"),
    path("solution", RagSolutionView.as_view(), name="rag-solution"),
    path("events", RagEventView.as_view(), name="rag-events"),
 

             
    path("dev/seed", DevSeedView.as_view(), name="dev-seed"),
    path("retrieve", RagRetrieveView.as_view(), name="rag-retrieve"),
]
