import pytest
from rest_framework import status
from unittest.mock import patch
from ..utils import user_valid_data

@pytest.mark.django_db
class TestUnitUserRegistrationApi:
    def test_user_registration_successful(self, api_client, mock_user, base_url):
        data = user_valid_data()
        data["password_confirm"] = data["password"]
        url = base_url+"register/"
        with patch("apps.users.services.user_service.UserService.register_user") as mock_register:
            mock_register.return_value = mock_user
            response = api_client.post(url, data, format="json")
 
            assert response.status_code == status.HTTP_201_CREATED
    
    @pytest.mark.parametrize("invalid_data", [
        {"email": "invalid-email", "username": "testuser", "password": "testpass123"},
        {"email": "test@example.com", "username": "t", "password": "testpass123"},
        {"email": "test@example.com", "username": "testuser", "password": "123"},
        {"email": "", "username": "testuser", "password": "testpass123"},
        {"username": "testuser", "password": "testpass123"}, 
    ])
    def test_user_registration_bad_request(self, api_client, base_url, invalid_data):
        url = base_url+"register/"
        response = api_client.post(url, invalid_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


