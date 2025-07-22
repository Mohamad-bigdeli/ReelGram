import pytest
import uuid
from django.contrib.auth import get_user_model
from .utils import user_valid_data
from unittest.mock import MagicMock
from ..services.token_service import TokenService

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
def mock_user() -> MagicMock:
    user = MagicMock()
    user.id = uuid.UUID('bf3f6dc2-3de7-4dc7-99f8-9c1f21a06c9a')
    user.email = "test@example.com"
    user.username = "testuser"
    return user

@pytest.fixture
def refresh_token_user_instance(user_instance) -> dict:
    refresh_token = TokenService.refresh_token(user_instance)
    return {"refresh_token":refresh_token, "user":user_instance}

@pytest.fixture
def login_data() -> dict:
    return {
        "email":"test1235@gmail.com",
        "password":"Aa123456@"
    }