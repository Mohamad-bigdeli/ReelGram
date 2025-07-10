from django.urls import path 
from . import views

app_name = "api-v1"

urlpatterns = [
    path("users/register/", views.UserRegistrationAPIView.as_view(), name="register")
]