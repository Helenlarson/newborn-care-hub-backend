from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  # remove username
    email = models.EmailField(unique=True)

    ROLE_CHOICES = [
        ("family", "Family"),
        ("provider", "Provider"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class FamilyProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="family_profile"
    )
    display_name = models.CharField(max_length=120)
    city = models.CharField(max_length=120, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
    due_date = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    photo = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.display_name
