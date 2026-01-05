from django.conf import settings
from langchain_community.chat_models import ChatOllama


def get_llm():
    return ChatOllama(
        base_url=settings.OLLAMA_BASE_URL,
        model=settings.OLLAMA_MODEL,
        temperature=0.2,
    )
