from django.urls import path
from users import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('verify_email/', views.VerifyEmailView.as_view()),
    path('refresh-token/', views.RefreshTokenView.as_view()),
    path('logout/', views.LogoutView.as_view())
]