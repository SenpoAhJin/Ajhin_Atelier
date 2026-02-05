from rest_framework import serializers
from .models import User

# Serializer used during registration
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        # Fields required for user creation
        fields = ('username', 'email', 'password', 'role')
        extra_kwargs = {
            'password': {'write_only': True}

        }

    def create(self, validated_data):
        # create user with hashed password
        user = User.objects.create_user(**validated_data)
        return user