# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class FamilyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="family_profile")
    display_name = models.CharField(max_length=120)
    city = models.CharField(max_length=80)
    zipcode = models.CharField(max_length=10)
    due_date = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="profiles/", blank=True, null=True)

    def __str__(self):
        return f"{self.display_name} ({self.user.email})"

