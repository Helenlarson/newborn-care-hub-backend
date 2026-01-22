
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class ServiceType(models.Model):
    # Ex: "Postpartum Doula", "Birth Doula", "Newborn Care Specialist", "Lactation Consultant"
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)

    def __str__(self):
        return self.name


class ProfessionalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="professional_profile")
    display_name = models.CharField(max_length=120)
    city = models.CharField(max_length=80)
    zipcode = models.CharField(max_length=10)
    bio = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)

    # Profissional pode oferecer mais de um serviço
    service_types = models.ManyToManyField(ServiceType, related_name="professionals", blank=True)

    photo = models.ImageField(upload_to="profiles/", blank=True, null=True)

    def __str__(self):
        return f"{self.display_name} ({self.user.email})"
