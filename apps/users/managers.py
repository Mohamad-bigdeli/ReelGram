from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):

    def create_user(self, email, username, password, **extra_fields):
        if not email and username:
            raise ValueError(_("Users must have an email and username"))
        user = self.model(
            email=self.normalize_email(email), 
            username=username, 
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is is_superuser=True"))
        if extra_fields.get("is_verified") is not True:
            raise ValueError(_("Superuser must have is is_verified=True"))
        return self.create_user(email, username, password, **extra_fields)
