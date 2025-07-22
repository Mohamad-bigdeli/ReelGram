import pytest
from rest_framework import status
from unittest.mock import patch, MagicMock
from ..utils import user_valid_data
from ...services.token_service import TokenService


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

@pytest.mark.django_db
class TestUnitUserLoginApi:
    @patch.object(TokenService, "access_token")
    @patch.object(TokenService, "refresh_token")
    def test_user_login_successful(self,mock_refresh, mock_access, api_client, base_url,
        user_instance):
        mock_access.return_value = "valid_access_token"
        mock_refresh.return_value = "valid_refresh_token"
        url = base_url+"login/"
        user = user_instance
        user_password = user_valid_data().get("password")
        data = {"email":user.email, "password":user_password}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["detail"]["status"] == "successful"
        assert response.data["detail"]["token"]["access_token"] == "valid_access_token"
        assert response.cookies["refresh_token"].value == "valid_refresh_token"
        
    @patch("apps.users.api.v1.views.auth.authenticate") 
    @patch("apps.users.api.v1.serializers.UserLoginSerializer")  
    def test_user_login_invalid_credentials(self, mock_serializer_class, mock_authenticate,
        login_data, base_url, api_client):
        url = base_url+"login/"
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.validated_data = login_data
        mock_serializer_class.return_value = mock_serializer
        mock_authenticate.return_value = None
        
        response = api_client.post(url, login_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['detail']['error'] == 'Invalid credentials'
    
    @patch.object(TokenService, "access_token")
    @patch.object(TokenService, "refresh_token")
    def test_user_login_token_service_failed(self,mock_refresh, mock_access, api_client, base_url,
        user_instance):
        mock_access.side_effect = Exception("Token generation failed")
        mock_refresh.side_effect = Exception("Token generation failed")
        url = base_url+"login/"
        user = user_instance
        user_password = user_valid_data().get("password")
        data = {"email":user.email, "password":user_password}
        response = api_client.post(url, data, format="json")
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"]["status"] == "failed"


@pytest.mark.django_db
class TestUnitUserLogoutApi:
    def test_user_logout_successful(self, api_client, base_url, mock_user):
        url = base_url+"logout/"
        with patch("apps.users.services.token_service.TokenService.blacklist_refresh_token") as mock_token_service:
            mock_token_service.return_value = None
            api_client.force_authenticate(user=mock_user) 
            response = api_client.get(url, HTTP_COOKIE='refresh_token=test_token')
            
            assert response.status_code == status.HTTP_200_OK
            assert response.data["detail"]["status"] == "successful"

    def test_user_logout_without_refresh_token(self, api_client, base_url, mock_user):
        url = base_url+"logout/"
        api_client.force_authenticate(user=mock_user)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
class TestUnitUserRefreshAccessToken:
    @patch.object(TokenService, "refresh_access_token")
    def test_user_refresh_access_token_successful(self, mock_refresh_access_token, api_client,
    base_url):
        url = base_url+"refresh/"
        mock_refresh_access_token.return_value = {"access_token":"new_valid_access", "refresh_token":"new_valid_refresh"}
        response = api_client.get(url, HTTP_COOKIE="refresh_token=older_refresh")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["detail"]["status"] == "successful"
        assert response.data["detail"]["token"]["access_token"] == "new_valid_access"
        assert response.cookies["refresh_token"].value == "new_valid_refresh"

    def test_refresh_access_token_not_set_refresh(self, api_client, base_url):
        url = base_url+"refresh/"
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    @patch("apps.users.services.token_service.TokenService.refresh_access_token")
    def test_refresh_access_token_invalid_refresh(self, mock_refresh_access_token,
        api_client, base_url):
        url = base_url+"refresh/"
        mock_refresh_access_token.side_effect = Exception("Invalid refresh token")
        response = api_client.get(url, HTTP_COOKIE='refresh_token=invalid_token')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"]["status"] == "failed"