from django.db import models


class EtmsUser(models.Model):
    """Model for User table"""
    DESIGNATION_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee')
    ]
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    designation = models.CharField(
        choices=DESIGNATION_CHOICES, max_length=20
    )


class Comments(models.Model):
    """Model used for storing comments by different users"""
    user = models.ForeignKey(EtmsUser, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)


class VerificationToken(models.Model):
    """Model for storing email verification tokens"""
    user = models.ForeignKey(EtmsUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=128, null=True, blank=True)
