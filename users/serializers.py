from rest_framework import serializers
from users.models import *


class UserSerializer(serializers.ModelSerializer):
    """Serilizer for User model"""

    class Meta:
        fields = '__all__'
        model = EtmsUser


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
