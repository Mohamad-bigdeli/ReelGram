import pytest
from django.contrib.auth import get_user_model
from .utils import user_valid_data


User = get_user_model()

@pytest.fixture
def user_instance():
    credentials = user_valid_data()
    user = User.objects.create(
        email=credentials["email"],
        username=credentials["username"]
    )
    user.set_password(credentials["password"])
    user.save()
    return user