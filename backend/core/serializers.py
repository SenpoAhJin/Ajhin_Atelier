from rest_framework import serializers
from .models import User, Order, DeclutterItem

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

# Serializer for displaying orders in dashboard list
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        # Only expose fields needed for dashboard performance
        fields = ('id', 'status', 'created_at')



# Serializer for account settings overview
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Editable fields for account settings
        fields = ('username', 'email')


# Serializer for creating and managing declutter listings
class DeclutterItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclutterItem

        # Expose only required fields
        fields = (
            'id',
            'title',
            'description',
            'condition',
            'quantity',
            'price',
            'is_active',
            'created_at'
        )

        read_only_fields = ('id', 'created_at')

    def create(self, validated_data):
        # Automatically assign the logged-in user as seller
        return DeclutterItem.objects.create(
            seller=self.context['request'].user,
            **validated_data
        )