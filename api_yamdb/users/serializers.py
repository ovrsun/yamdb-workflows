from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'bio', 'role',
        )
        model = CustomUser


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = (
            'username', 'confirmation_code',
        )
        model = CustomUser


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        r"^[\w.@+-]+\Z$",
        max_length=150,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all())
        ]
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all())
        ]
    )

    def validate_username(self, value):
        if value.lower() == settings.DEFAULT_NAME:
            raise serializers.ValidationError(
                f"Username {settings.DEFAULT_NAME} is not valid")
        return value

    class Meta:
        fields = ("username", "email")
        model = CustomUser
