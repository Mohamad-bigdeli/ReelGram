from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django.core.validators import RegexValidator, EmailValidator
from django.utils.translation import gettext_lazy as _


User = get_user_model()

class UserService:

    @staticmethod
    def register_user(email: str, username: str, password:str) -> User:
        try:
            UserService._validate_registration_data(email, username, password)
            UserService._check_uniques_data(email, username)       
            with transaction.atomic():
                user = User.objects.create_user(email=email, username=username, password=password)
                return user
        except ValidationError as e:
            raise ValidationError(f"Registration failed : {e}")
        
    @staticmethod
    def _validate_registration_data(email: str, username: str, password:str) -> None:

        errors = []

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
        
        if errors:
            raise ValidationError(errors)
    
    @staticmethod
    def _check_uniques_data(email: str, username: str) -> None:

        errors = []

        if User.objects.filter(email=email).exists():
            errors.append("The email entered is a duplicate.")
        if User.objects.filter(username=username).exists():
            errors.append("The username entered is a duplicate.")

        if errors:
            raise ValidationError(errors)