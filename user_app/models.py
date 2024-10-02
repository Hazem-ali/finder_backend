from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("email is required")
        if not password:
            raise ValueError("password is required")

        # If these fields don't exist, set them to false, else pass their original value
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user = self.model(email=self.normalize_email(email), **extra_fields)
        
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractUser):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254, unique=True)

    # TODO make is_supervisor default to be False
    is_supervisor = models.BooleanField(default=True)
    role = models.CharField(max_length=50)

    password = models.CharField(max_length=255)

    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.get_name()
