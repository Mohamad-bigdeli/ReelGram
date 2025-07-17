from rest_framework import serializers
from django.core.validators import EmailValidator, RegexValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ValidationError
from django.utils.translation import gettext_lazy as _

class UserRegistrationSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)
    username = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True)
    password_confirm = serializers.CharField(max_length=255, required=True)

    def validate(self, attrs):  
        errors = []
        email = attrs.get("email")
        username = attrs.get("username")
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")

        email_validator = EmailValidator()
        try:
            email_validator(email)
        except ValidationError:
            errors.append("Please enter a valid email address")

        username_validator = RegexValidator(regex=r'^[a-zA-Z0-9_]+$',
        message=_('Username can only contain letters, numbers, and underscores'))
        try:
            username_validator(username)
        except ValidationError as e:
            errors.append(str(e))
        if len(username) < 3:
            errors.append("Username must be at least 3 characters long")
        if len(username) > 30:
            errors.append("Username cannot exceed 30 characters")

        try:
            validate_password(password)
        except ValidationError as e:
            errors.extend(e.messages)
        
        if password != password_confirm:
            errors.append("Passwords dose not match.")
        
        if errors:
            raise ValidationError(errors)
    
        return super().validate(attrs)

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, max_length=255)

    def validate(self, attrs):
        errors = []
        email = attrs.get("email")
        password = attrs.get("password")
        try:
            EmailValidator(email)
        except ValidationError:
            errors.append("Please enter a valid email address")
        try:
            validate_password(password)
        except ValidationError as e:
            errors.extend(e.messages)
        if errors:
            raise ValidationError(errors)
        return super().validate(attrs)