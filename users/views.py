import jwt

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.conf import settings

from users.models import EtmsUser, UserToken
from users.serializers import *
from users.utils import send_verification_mail, generate_tokens


class RegisterAPIView(APIView):
    """Class for registering a new user"""
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """POST request for user registration"""
        # try:
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
        
        # except Exception as e:
        #     error = "Error creating User. Please try again." + str(e)
        #     return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)


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
        
            user = authenticate(username=username, password=password)

            if not user:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            if user.is_active:
                access_token, refresh_token = generate_tokens(user)

                UserToken.objects.update_or_create(
                    user=user, defaults={
                        "access_token": access_token, "refresh_token": refresh_token
                    }
                )

                return Response({
                    "access_token": access_token,
                    "refresh_token": refresh_token
                })
            
            error = "User inactive! Please contact admin."
            return Response({"error": error}, status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response(
                {"error": "Something went wrong. " + str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class RefreshTokenView(APIView):
    """Class to refresh the user tokens"""
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            payload = jwt.decode(
                serializer.validated_data['refresh_token'], settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM]
            )

            if payload["type"] != "refresh":
                raise jwt.InvalidTokenError

            user_id = payload["user_id"]
            user = EtmsUser.objects.get(id=user_id)

            access_token, refresh_token = generate_tokens(user)

            UserToken.objects.update_or_create(
                user=user,
                defaults={
                    "access_token": access_token, "refresh_token": refresh_token
                }
            )

            return Response({
                "access_token": access_token,
                "refresh_token": refresh_token
            })

        except jwt.ExpiredSignatureError:
            return Response(
                {"error": "Refresh token expired"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        except jwt.InvalidTokenError:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token_obj = UserToken.objects.get(user=request.user)
            token_obj.delete()
            return Response(
                {"message": "Logged out and tokens revoked."},
                status=status.HTTP_200_OK
            )
        
        except UserToken.DoesNotExist:
            return Response(
                {"error": "No active tokens found."},
                status=status.HTTP_400_BAD_REQUEST
            )
