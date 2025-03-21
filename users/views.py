from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator

from users.models import EtmsUser
from users.serializers import *
from users.utils import send_verification_mail


class RegisterAPIView(APIView):
    """Class for registering a new user"""
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """POST request for user registration"""
        try:
            data = request.data
            print("request data", data)
            serializer = UserSerializer(data=data)

            if serializer.is_valid():
                print("validated data", serializer.validated_data)
                
                if EtmsUser.objects.filter(email=request.data['email']):
                    error = "Account already exists! Please login"
                    return Response(
                        {"error": error}, status=status.HTTP_400_BAD_REQUEST
                    )
                user = serializer.save(
                    password=make_password(serializer.validated_data['password'])
                )
                print("after save...")
                print(user)
                send_verification_mail(request, user)
                message = "User created successfully!"
                return Response({"message": message}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            error = "Error creating User. Please try again." + str(e)
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """Class for loging in an user"""
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """POST request for login method"""
        username = request.data.get("username", None)
        password = request.data.get("password", None)

        try:
            if not username or not password:
                error = "Username and password are required!"
                return Response(
                    {"error": error}, status=status.HTTP_400_BAD_REQUEST
                )
        
            user = EtmsUser.objects.get(username=username, password=password)

            if user:
                return Response(
                    {"message": "Login Successful!"}, status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {"error": "User does not exists! " + str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class VerifyEmailView(APIView):
    """API to verify new registered user email"""
    authentication_classes = []
    permission_classes = [AllowAny]

    def patch(self, request, *args, **kwargs):
        """GET request to verify user email"""
        user = request.data.get("user", None)
        token = request.data.get("token", None)

        if not user or not token:
            error = "User details and secret token are required!"
            return Response(
                {"error": error}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            verify_obj = VerificationToken.objects.get(user=user, token=token)

            if verify_obj:
                user_obj = EtmsUser.objects.get(id=user)
                user_obj.is_active = True
                user_obj.save()
                verify_obj.delete()
                message = "Account successfully verified."
                return Response(
                    {"message": message}, status=status.HTTP_200_OK
                )
            
            error = "Error verifying email"
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
        
        except VerificationToken.DoesNotExist:
            return Response(
                {"error": "Link expired!"}, status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            return Response(
                {"error": "Sommething went wrong! " + str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
