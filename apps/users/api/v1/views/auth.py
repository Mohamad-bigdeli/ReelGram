from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ....services.user_service import UserService
from ....services.token_service import TokenService
from ..serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer,)
from rest_framework.response import Response
from rest_framework import status
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate

class UserRegistrationAPIView(APIView):
    
    @method_decorator(ratelimit(key="user_or_ip", rate="5/m", method="POST", block=True))
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user_service = UserService()
            user = user_service.register_user(
                email=serializer.validated_data["email"],
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"]
            )
            return Response({"detail":{
                "status":"successful", 
                "user":{
                    "id":user.id,
                    "email":user.email,
                    "username":user.username
                },
            }}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail":{
                "status":"failed",
                "error":f"{e}"
            }}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):

    @method_decorator(ratelimit(key="user_or_ip", rate="5/m", method="POST", block=True))
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(username=email, password=password)
        if not user:
            return Response({"detail":{
                "error":"Invalid credentials"
            }}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            access_token = TokenService.access_token(user)
            refresh_token = TokenService.refresh_token(user)

            response = Response({"detail":{
                "status":"successful",
                "user":{
                    "id":user.id,
                    "email":user.email,
                    "username":user.username
                },
                "token":{
                    "access_token":access_token,
                    "token_type":"Bearer",
                    "expires_in":1800
                }
            }}, status=status.HTTP_200_OK)
            response.set_cookie(
                'refresh_token',
                refresh_token,
                max_age=7*24*60*60, 
                httponly=True,
                secure=False,
                samesite='Lax',
                path='/'
            )
            return response
        
        except Exception as e:
            return Response({"detail":{
                "status":"failed",
                "error":f"{e}"}}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class UserLogOutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            try:
                TokenService.blacklist_refresh_token(refresh_token)
            except Exception:
                pass
        response = Response({"detail":{
            "status":"successful",
        }})
        response.delete_cookie("refresh_token")
        return response

class UserRefreshTokenAPIView(APIView):

    @method_decorator(ratelimit(key="user_or_ip", rate="5/m", method="POST", block=True))
    def get(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"detail":{
                "status":"failed",
                "error":"refresh token not be set."
            }}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            new_tokens = TokenService.refresh_access_token(refresh_token)

            response = Response({"detail":{
                "status":"successful",
                "token":{
                    "access_token":new_tokens["access_token"]
                }
            }}, status=status.HTTP_200_OK)
            response.set_cookie(
                'refresh_token',
                new_tokens["refresh_token"],
                max_age=7*24*60*60, 
                httponly=True,
                secure=False,
                samesite='Lax',
                path='/'
            )
            return response
        except Exception as e:
            return Response({"detail":{
                "status":"failed",
                "error":f"{e}"}}, 
                status=status.HTTP_400_BAD_REQUEST
            )