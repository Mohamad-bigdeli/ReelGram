from django.urls import path 
from . import views

app_name = "api-v1"

urlpatterns = [
    path("users/register/", views.UserRegistrationAPIView.as_view(), name="register"),
    path("users/login/", views.UserLoginAPIView.as_view(), name="login"),
    path("users/logout/", views.UserLogOutAPIView.as_view(), name="logout"), 
    path("users/refresh/", views.UserRefreshTokenAPIView.as_view(), name="refresh"),
]