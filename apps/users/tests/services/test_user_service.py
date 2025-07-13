import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from ...services.user_service import UserService
from ..utils import user_valid_data, user_invalid_data

User = get_user_model()

@pytest.mark.django_db
class TestUserService:
    def test_user_registration_success(self):
        data = user_valid_data()
        user = UserService.register_user(**data)
        assert user.email == data["email"]
        assert user.username == data["username"]
        assert user.check_password(data["password"])
        assert User.objects.filter(id=user.id).exists()

    @pytest.mark.parametrize(
        "email,username,password", [
            ("not-an-email", "a!", "123"),
            ("test@", "very_long_username_that_exceeds_thirty_characters_limit", "password")
        ]       
    )
    def test_user_registration_fail(self, email, username, password):
        with pytest.raises(ValidationError):
            UserService.register_user(email, username, password)

    def test_validation_register_data_success(self):
        data = user_valid_data()
        try:
            UserService._validate_registration_data(**data)
        except ValidationError:
            pytest.fail("Validation should not raise error for valid data")

    def test_validation_register_data_fail(self):
        data = user_invalid_data()
        with pytest.raises(ValidationError) as errors:
            UserService._validate_registration_data(**data)
        errors_message = str(errors.value)
        assert "Please enter a valid email address" in errors_message
        assert "Username can only contain letters, numbers, and underscores" in errors_message
        assert "This password is too short. It must contain at least 8 characters." in errors_message
    def test_check_unique_data(self):
        data = user_valid_data()
        try:
            UserService._check_uniques_data(email=data["email"], username=data["username"])
        except ValidationError:
            pytest.fail("Uniqueness check should not raise error for new data")

    def test_check_unique_data_fail(self):
        data = user_valid_data()
        UserService.register_user(**data)
        with pytest.raises(ValidationError) as exc_info:
            UserService._check_uniques_data(email=data["email"], username=data["username"])
        
        error_message = str(exc_info.value)
        assert "The email entered is a duplicate." in error_message
        assert "The username entered is a duplicate." in error_message
