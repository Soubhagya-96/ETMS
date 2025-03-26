from django.contrib.auth.models import BaseUserManager

class EtmsUserManager(BaseUserManager):
    """Custom manager for EtmsUser model"""

    def create_user(self, username, password=None, **extra_fields):
        """Creates and returns a regular user"""
        if not username:
            raise ValueError("The Username field must be set")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """Creates and returns a superuser"""
        extra_fields.setdefault("is_active", True)

        return self.create_user(username, password, **extra_fields)
