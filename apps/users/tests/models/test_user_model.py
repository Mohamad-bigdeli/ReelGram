import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from ..utils import user_valid_data, user_invalid_data

User = get_user_model()

@pytest.mark.django_db
class TestUserModel:
    def test_create_user_valid_data(self):
        credentials = user_valid_data()
        user = User.objects.create(
            email=credentials["email"],
            username=credentials["username"]
        )
        user.set_password(credentials["password"])
        user.save()
        assert user.email == credentials["email"]
        assert user.username == credentials["username"]
        assert user.check_password(credentials["password"])

    def test_create_user_invalid_data(self):
        credentials = user_invalid_data()
        with pytest.raises(ValidationError):
            user = User.objects.create(
                email=credentials["email"],
                username=credentials["username"]
            )
            user.set_password(credentials["password"])
            user.full_clean()
            user.save()


    def test_get_user_by_id(self, user_instance):
        get_user = User.objects.get(id=user_instance.id)
        assert get_user == user_instance


    def test_user_str(self, user_instance):
        assert str(user_instance) == user_instance.username