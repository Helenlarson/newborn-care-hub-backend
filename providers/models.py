from django.conf import settings
from django.db import models


class ProfessionalProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="professional_profile"
    )

    display_name = models.CharField(max_length=120)
    headline = models.CharField(max_length=200, blank=True)
    service_types = models.JSONField(default=list, blank=True)

    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    photo = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.display_name


class ServiceType(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)

    def __str__(self):
        return self.name
