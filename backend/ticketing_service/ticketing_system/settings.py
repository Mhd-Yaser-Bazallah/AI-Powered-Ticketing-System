from datetime import timedelta
from pathlib import Path
import os 
from dotenv import load_dotenv

                                           
load_dotenv()
                                                                
BASE_DIR = Path(__file__).resolve().parent.parent



                                                              
                                                                       

                                                                  
SECRET_KEY = 'django-insecure-*(gi@#+_+4**japd8b1lvqi$84awp$aqwy%!8hd7o$y23szs%l'

                                                                 
DEBUG = False

ALLOWED_HOSTS = []


                        

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
                      
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',                              
    
             
     'workflow_management',
    'authentication',
    'users_management',
    'company',
    'team',
    'ticket',
    'ticket_log',
    'notification',
    'comments',
    'reporting',
    'analysis',
    'files',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'ticketing_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ticketing_system.wsgi.application'


          
                                                               

DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': '3306',
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


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.1.106', '55a9a57542ec.ngrok-free.app',]

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5173",
    "https://192.168.1.106", 
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "http://localhost:8000",
    "https://55a9a57542ec.ngrok-free.app",
]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:5173",
    "https://192.168.1.106", 
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "http://localhost:8000",
    "https://55a9a57542ec.ngrok-free.app",
]
 
                                                           
CORS_ALLOW_CREDENTIALS = True
CORS_DEBUG = True
 

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

RAG_API_KEY = os.getenv("RAG_API_KEY", "")
ANALYZE_SERVICE_BASE_URL = os.getenv("ANALYZE_SERVICE_BASE_URL", "http://127.0.0.1:8002")
