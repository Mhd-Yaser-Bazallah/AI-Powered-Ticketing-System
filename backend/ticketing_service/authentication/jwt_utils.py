import jwt
from django.conf import settings
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
 
load_dotenv()

def get_tokens_for_user(user):
    payload = {
        'user_id': user.id,  
        'role': user.role,    
        'exp': datetime.utcnow() + timedelta(hours=24),  
        'iat': datetime.utcnow(), 
    } 
     
    token = jwt.encode(payload, os.getenv("JWT_SECRET"), algorithm='HS256')
    

    if isinstance(token, bytes):
        token = token.decode('utf-8')
        
     
    return  token