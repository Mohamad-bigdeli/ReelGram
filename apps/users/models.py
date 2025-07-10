from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
import uuid

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(
        max_length=225, unique=True,
        validators=[RegexValidator(regex=r'^[a-zA-Z0-9_]+$',
        message=_('Username can only contain letters, numbers, and underscores'))]
    )

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    REQUIRED_FIELDS = ["username"]
    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.username
    class Meta:
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['email']),
            models.Index(fields=['username']),
            models.Index(fields=["is_verified"]),
        ]

def profile_picture_upload_path(instance, filename):
    return f'profiles/{instance.user.id}/{filename}'

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=355, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to=profile_picture_upload_path, null=True, blank=True)
    follower_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
        ]