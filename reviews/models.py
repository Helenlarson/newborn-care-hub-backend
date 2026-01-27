from django.db import models
from django.conf import settings
from providers.models import ProfessionalProfile


class Review(models.Model):
    professional = models.ForeignKey(
        ProfessionalProfile,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    family_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews_written"
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Review {self.rating} for {self.professional_id}"
