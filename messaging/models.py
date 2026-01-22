# Create your models here.
from django.db import models
from providers.models import ProfessionalProfile

class Message(models.Model):
    professional = models.ForeignKey(
        ProfessionalProfile,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    family_name = models.CharField(max_length=120)
    family_email = models.EmailField()
    family_city = models.CharField(max_length=80, blank=True)
    family_zipcode = models.CharField(max_length=10, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Msg to prof {self.professional_id} from {self.family_email}"
