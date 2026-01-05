import os
from pathlib import Path

from dotenv import load_dotenv
from corsheaders.defaults import default_headers

                                                                
BASE_DIR = Path(__file__).resolve().parent.parent


                                                              
                                                                       

                                                                  
SECRET_KEY = 'django-insecure-$7(1oupr@vm24(c#-wm#*4cg)-7-vmx%5$l7_r=$60%+x_#r4*'

                                                                 
DEBUG = True

ALLOWED_HOSTS = []


                        

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rag',
    'corsheaders',
]
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
RAG_API_KEY = os.getenv("RAG_API_KEY", "")

QDRANT_URL = os.getenv("QDRANT_URL", "http://127.0.0.1:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "kb_main")

EMBEDDINGS_PROVIDER = os.getenv("EMBEDDINGS_PROVIDER", "local")
EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", "all-MiniLM-L6-v2")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
RERANK_ENABLED = os.getenv("RERANK_ENABLED", "true").lower() == "true"
RERANK_MODEL = os.getenv("RERANK_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")

RAG_RETRIEVE_K = int(os.getenv("RAG_RETRIEVE_K", "12"))
RAG_TOP_K = int(os.getenv("RAG_TOP_K", "4"))
CHAT_LAST_N = int(os.getenv("CHAT_LAST_N", "12"))
SUMMARY_EVERY_N = int(os.getenv("SUMMARY_EVERY_N", "8"))

RAG_MIN_SCORE = float(os.getenv("RAG_MIN_SCORE", "0.25"))
RAG_TOP_K = int(os.getenv("RAG_TOP_K", "6"))

CELERY_BROKER_URL = os.getenv("RAG_BROKER_URL") or os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
CELERY_TASK_DEFAULT_QUEUE = os.getenv("RAG_TASK_QUEUE", "rag_events")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"

RAG_FILES_BASE_PATH = os.getenv("RAG_FILES_BASE_PATH", "")

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = 'rag_ms.urls'
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [],
}
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rag_ms.wsgi.application'


          
                                                               

_db_name = os.getenv("DB_NAME")
if _db_name:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": _db_name,
            "USER": os.getenv("DB_USER", ""),
            "PASSWORD": os.getenv("DB_PASSWORD", ""),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", "3306"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


                     
                                                                              

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


                      
                                                    

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


                                        
                                                           

STATIC_URL = 'static/'

                                
                                                                        

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]



CORS_ALLOW_HEADERS = list(default_headers) + [
    "x-rag-api-key",
]
