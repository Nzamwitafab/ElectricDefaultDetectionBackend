# core/serializers.py
from rest_framework import serializers
from core.models import User

class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=20)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long.")
        return value
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long.")
        return value
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'phone_number', 'role','password']  # Add other fields if needed

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['email', 'name', 'phone_number', 'role']  # Add other fields for updating if needed
        read_only_fields = ['id']  # Prevent updating the 'id'