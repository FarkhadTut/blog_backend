from rest_framework import serializers
from .models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'bio', 'profile_picture', ]
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

        