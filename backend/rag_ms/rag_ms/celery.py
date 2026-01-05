import logging
import os

                                                
try:
    from dotenv import load_dotenv
    load_dotenv()                                             
except Exception:
                                                                           
    pass

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rag_ms.settings")

app = Celery("rag_ms")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

logger = logging.getLogger(__name__)

                                                                     
from django.conf import settings                                       

logger.info("Celery broker=%s default_queue=%s", getattr(settings, "CELERY_BROKER_URL", "missing"), getattr(settings, "CELERY_TASK_DEFAULT_QUEUE", "missing"))
logger.info(
    "RAG settings: RETRIEVE_K=%s TOP_K=%s MIN_SCORE=%s RERANK_ENABLED=%s",
    getattr(settings, "RAG_RETRIEVE_K", "missing"),
    getattr(settings, "RAG_TOP_K", "missing"),
    getattr(settings, "RAG_MIN_SCORE", "missing"),
    getattr(settings, "RERANK_ENABLED", "missing"),
)
logger.info("ENV CHECK: QDRANT_URL=%s", os.getenv("QDRANT_URL"))
