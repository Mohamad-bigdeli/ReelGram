from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class TokenService:
    
    @staticmethod
    def access_token(user: User) -> str:
        if not user:
            raise ValidationError("User is required.")
        try:
            token = AccessToken.for_user(user)
            return str(token)
        except Exception as e:
            raise ValidationError(f"Failed create access token:{e}")
    
    @staticmethod
    def refresh_token(user: User) -> str:
        if not user:
            raise ValidationError("User is required.")
        try:
            token = RefreshToken.for_user(user)
            return str(token)
        except Exception as e:
            raise ValidationError(f"Failed create refresh token:{e}")
    
    @staticmethod
    def refresh_access_token(token: str) -> dict:
        if not token:
            raise ValidationError("Refresh token is required.")
        try:
            refresh_token = RefreshToken(token)
            refresh_token.check_exp()
            new_access_token = str(refresh_token.access_token)
            new_refresh_token = str(refresh_token) if refresh_token else token
            return {"access_token":new_access_token, "refresh_token":new_refresh_token}
        except Exception as e:
            raise ValidationError(f"Failed refresh access token:{e}")

    @staticmethod
    def verify_access_token(token: str) -> bool:
        if not token:
            raise ValidationError("Token is required.")
        access_token = AccessToken(token)
        try:
            access_token.check_exp()
            user_id = access_token.payload.get("user_id")
            if not user_id:
                raise ValidationError("Invalid token payload.")
            user = User.objects.get(id=user_id)
            if not user.is_active:
                raise ValidationError("User account is disabled.")
            return True
        except Exception as e:
            raise ValidationError(f"Failed verifying:{e}")
    
    @staticmethod
    def verify_refresh_token(token: str) -> bool:
        if not token:
            raise ValidationError("Token is required.")
        refresh_token = RefreshToken(token)
        try:
            refresh_token.check_exp()
            user_id = refresh_token.payload.get("user_id")
            if not user_id:
                raise ValidationError("Invalid token payload.")
            user = User.objects.get(id=user_id)
            if not user.is_active:
                raise ValidationError("User account is disabled.")
            return True
        except Exception as e:
            raise ValidationError(f"Failed verifying:{e}")

        
    @staticmethod
    def blacklist_refresh_token(token: str) -> None:
        if not token:
            raise ValidationError("Token is required.")
        try:
            RefreshToken(token).blacklist()
        except Exception as e:
            raise ValidationError(f"error:{e}")
        