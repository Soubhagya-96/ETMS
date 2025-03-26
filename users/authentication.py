import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import EtmsUser

class CustomJWTAuthentication(BaseAuthentication):
    """Custom JWT authentication for Django REST Framework"""
    
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None  # No authentication attempt, move to the next auth class
        
        token = auth_header.split(" ")[1]

        try:
            # Decode JWT token
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
            
            # Retrieve user from token payload
            user = EtmsUser.objects.get(id=payload["user_id"])

            if not user.is_active:
                raise AuthenticationFailed("User is inactive")

            return (user, None)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")
        except EtmsUser.DoesNotExist:
            raise AuthenticationFailed("User not found")
