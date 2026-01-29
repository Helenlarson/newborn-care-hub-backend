from django.db import models
from django.conf import settings


class Conversation(models.Model):
    professional = models.ForeignKey(
        "accounts.ProfessionalProfile",
        on_delete=models.CASCADE,
        related_name="conversations"
    )
    family_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="conversations"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("professional", "family_user")]
        ordering = ["-updated_at"]

    def __str__(self):
        return f"Conv prof={self.professional_id} family={self.family_user_id}"


class Message(models.Model):
    SENDER_CHOICES = [
        ("family", "Family"),
        ("provider", "Provider"),
    ]

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
        null=True,
        blank=True,
    )
    sender_role = models.CharField(max_length=20, choices=SENDER_CHOICES,  default="family")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # opcional (muito útil para inbox)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Msg {self.sender_role} conv={self.conversation_id}"
