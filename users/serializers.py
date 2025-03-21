from rest_framework.serializers import ModelSerializer
from users.models import *


class UserSerializer(ModelSerializer):
    """Serilizer for User model"""

    class Meta:
        fields = '__all__'
        model = EtmsUser

