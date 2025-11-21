from flask import request
import jwt
from config import SECRET_JWT_KEY
from functools import wraps

def token_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
    
        if not auth_header:
            return {'error': 'no token'}, 401
        
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return {'error': 'invalid token'}, 401
        
        try:
            payload = jwt.decode(token, SECRET_JWT_KEY, algorithms=['HS256'])
            request.current_user = payload
            
        except jwt.ExpiredSignatureError:
            return {"error": "expred"}, 401
        except jwt.InvalidTokenError:
            return {"error": "invalid"}, 401
        
        return func(*args, **kwargs)
        
    return wrapper

def role_required(*allowed_roles):
    def decorator(func):
        @wraps(func)
        @token_required
        def wrapper(*args, **kwargs):
            payload = request.current_user
            role = payload.get('user_role')
            
            if not role or role not in allowed_roles:
                return {
                    'error': f"insufficient permission for the role {role}"
                }, 403
                
            return func(*args, **kwargs)
        return wrapper
    
    return decorator