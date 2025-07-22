import pytest
from rest_framework import status
from django.contrib.auth import get_user_model
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

@pytest.mark.django_db
class TestIntegrationUserLoginApi:
    def test_user_login_successful(self, api_client, base_url, user_instance):
        user_email = user_instance.email
        user_password = user_valid_data().get("password")
        url = base_url+"login/"
        data = {"email":user_email, "password":user_password}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["detail"]["status"] == "successful"
        assert "access_token" in response.data["detail"]["token"]
        assert "refresh_token" in response.cookies

    def test_user_login_invalid_credentials(self, api_client, base_url):
        url = base_url+"login/"
        user_data = user_valid_data()
        data = {"email":user_data["email"], "password":user_data["password"]}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"]["error"] == "Invalid credentials"


@pytest.mark.django_db
class TestIntegrationUserLogoutApi:
    def test_user_logout_successful(self, base_url, api_client, refresh_token_user_instance):
        refresh_token = refresh_token_user_instance["refresh_token"]
        url = base_url+"logout/"
        api_client.force_authenticate(refresh_token_user_instance["user"])
        response = api_client.get(url, HTTP_COOKIE=f"refresh_token={refresh_token}")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["detail"]["status"] == "successful"

@pytest.mark.django_db
class TestIntegrationUserRefreshAccessTokenApi:
    def test_user_refresh_access_token_successful(self, api_client, base_url, refresh_token_user_instance):
        url = base_url+"refresh/"
        refresh_token = refresh_token_user_instance["refresh_token"]
        response = api_client.get(url, HTTP_COOKIE=f"refresh_token={refresh_token}")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["detail"]["status"] == "successful"
        assert "access_token" in response.data["detail"]["token"]
        assert response.data["detail"]["token"]["token_type"] == "Bearer"
        assert "refresh_token" in response.cookies

    def test_user_refresh_access_token_without_cookie(self, api_client, base_url):
        url = base_url+"refresh/"
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_refresh_access_token_invalid_cookie(self, api_client, base_url, refresh_token_user_instance):
        url = base_url+"refresh/"
        invalid_refresh = refresh_token_user_instance["refresh_token"]+"invalid"
        response = api_client.get(url, HTTP_COOKIE=f"refresh_token={invalid_refresh}")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"]["status"] == "failed"
