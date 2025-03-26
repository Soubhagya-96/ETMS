from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers import EtmsUserManager

class EtmsUser(AbstractBaseUser, PermissionsMixin):
    """Model for User table"""
    DESIGNATION_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee')
    ]
    username = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    designation = models.CharField(
        choices=DESIGNATION_CHOICES, max_length=20
    )

    objects = EtmsUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username


class Comments(models.Model):
    """Model used for storing comments by different users"""
    user = models.ForeignKey(EtmsUser, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)


class VerificationToken(models.Model):
    """Model for storing email verification tokens"""
    user = models.ForeignKey(EtmsUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=128, null=True, blank=True)


class UserToken(models.Model):
    """Model for storing access and refresh token details"""
    user = models.ForeignKey(EtmsUser, on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
