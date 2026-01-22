# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from providers.models import ProfessionalProfile

class Review(models.Model):
    professional = models.ForeignKey(
        ProfessionalProfile,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    family_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews_written"
    )
    rating = models.PositiveSmallIntegerField()  # 1..5 (vamos validar no serializer)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Review {self.rating} for {self.professional_id}"

