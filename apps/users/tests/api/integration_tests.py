import pytest
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from ..utils import user_valid_data, user_invalid_data


User = get_user_model()

@pytest.mark.django_db
class TestIntegrationUserRegistrationApi: 
    def test_user_register_successful(self, api_client, base_url):
        data = user_valid_data()
        data["password_confirm"] = data["password"]
        url = base_url+"register/"
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        user = User.objects.get(id=response.data["detail"]["user"]["id"])
        assert user.username == data["username"]
        assert user.check_password(data["password"])
    
    def test_user_register_fail(self, api_client, base_url):
        data = user_invalid_data()
        data["password_confirm"] = "deferent-password"
        url = base_url+"register/"
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.parametrize("duplicate_data", [
        {"email":"example@test.com", "username":"Testuser456", "password":"Aa123456@"},
        {"email":"example123@test.com", "username":"Testuser123", "password":"Aa123456@"},
    ])
    def test_user_register_with_duplicate_data(self, api_client, base_url, duplicate_data):
        user = User.objects.create(email="example@test.com", username="Testuser123")
        user.set_password("Aa123456@")
        user.save()
        url = base_url+"register/"
        response = api_client.post(url, duplicate_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "The email entered is a duplicate." or "The username entered is a duplicate." == response.data["detail"]["error"]
