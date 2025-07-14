import pytest
from django.contrib.auth import get_user_model
from .utils import user_valid_data
from unittest.mock import MagicMock

User = get_user_model()

@pytest.fixture
def user_instance() -> User:
    credentials = user_valid_data()
    user = User.objects.create(
        email=credentials["email"],
        username=credentials["username"]
    )
    user.set_password(credentials["password"])
    user.save()
    return user

@pytest.fixture(scope="session")
def base_url() -> str:
    return "http://127.0.0.1:8000/api/v1/users/"

@pytest.fixture
def mock_user():
    user = MagicMock()
    user.id = 1
    user.email = "test@example.com"
    user.username = "testuser"
    return user