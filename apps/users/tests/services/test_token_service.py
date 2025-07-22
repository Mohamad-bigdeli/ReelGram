import pytest 
from ...services.token_service import TokenService
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

@pytest.mark.django_db
class TestTokenService:
    def test_access_token_success(self, user_instance):
        access_token = TokenService.access_token(user_instance)
        user_id = AccessToken(access_token).payload.get("user_id")
        assert str(user_instance.id) == user_id

    def test_access_token_fail(self):
        with pytest.raises(ValidationError):
            TokenService.access_token(None)
        
    def test_refresh_token_success(self, user_instance):
        refresh_token = TokenService.refresh_token(user_instance)
        user_id = RefreshToken(refresh_token).payload.get("user_id")
        assert str(user_instance.id) == user_id

    def test_refresh_token_fail(self):
        with pytest.raises(ValidationError):
            TokenService.refresh_token(None)

    def test_refresh_access_token_success(self, refresh_token_user_instance):
        new_tokens = TokenService.refresh_access_token(refresh_token_user_instance["refresh_token"])
        new_access = new_tokens["access_token"]
        user_id = AccessToken(new_access).payload.get("user_id")
        assert str(refresh_token_user_instance["user"].id) == user_id


    @pytest.mark.parametrize("invalid_refresh_token", [
        "", 
        None, 
        "invalid-refresh-token", 
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.invalid",
        "expired.token.here" 
    ])
    def test_refresh_access_token_fail(self, invalid_refresh_token):
        with pytest.raises(ValidationError):
            TokenService.refresh_access_token(invalid_refresh_token)

    def test_blacklist_refresh_token(self, refresh_token_user_instance):
        TokenService.blacklist_refresh_token(refresh_token_user_instance["refresh_token"])
        with pytest.raises(ValidationError):
            TokenService.refresh_access_token(refresh_token_user_instance["refresh_token"])