import random
import string
import jwt
from datetime import datetime, timedelta

from django.core.mail import send_mail
from django.conf import settings
from users.models import EtmsUser, Comments, VerificationToken

def send_verification_mail(request, user):
    """
    This method is used to send email to verify new registered email address
    """
    secret = settings.JWT_SECRET
    email_from = settings.EMAIL_HOST_USER
    token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    encoded = jwt.encode(
        {"user": user.id, "token": token}, secret, algorithm="HS256"
    )
    url = request.META.get("HTTP_REFERER")
    subject = "Verify Your email"
    
    body = """
    Hi {},\n\n
    Click the link below to verify your email:
    {}register?verify={}\n\n
    If you did not request this, ignore this email.
    """.format(user.first_name, url, encoded)

    recipient_list = [user.email, ]
    result = send_mail(subject, body, email_from, recipient_list)
    new_token = VerificationToken(
        token = token
    )
    new_token.user = user
    new_token.save()
    print(result)

def generate_tokens(user):
    payload_access = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.now() + settings.JWT_ACCESS_EXPIRY,
        "type": "access"
    }
    payload_refresh = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.now() + settings.JWT_REFRESH_EXPIRY,
        "type": "refresh"
    }

    access_token = jwt.encode(
        payload_access, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    refresh_token = jwt.encode(
        payload_refresh, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )

    return access_token, refresh_token
