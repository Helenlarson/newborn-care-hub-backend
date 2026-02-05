from rest_framework import serializers
from .models import Conversation, Message


class ContactCreateSerializer(serializers.Serializer):
    professional_id = serializers.IntegerField()
    message = serializers.CharField()


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    sender_user_id = serializers.SerializerMethodField()
    sender_professional_id = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "id",
            "sender_role",
            "sender_name",
            "sender_user_id",
            "sender_professional_id",
            "body",
            "created_at",
            "is_read",
        ]

    def get_sender_name(self, obj: Message):
        conv = obj.conversation
        if not conv:
            return None

        if obj.sender_role == "provider":
            # ProfessionalProfile.display_name
            return getattr(conv.professional, "display_name", None) or "Profissional"

        # family
        fam_user = conv.family_user
        fam_profile = getattr(fam_user, "family_profile", None)
        return (
            getattr(fam_profile, "display_name", None)
            or getattr(fam_user, "email", None)
            or "Familiar"
        )

    def get_sender_user_id(self, obj: Message):
        conv = obj.conversation
        if not conv:
            return None

        if obj.sender_role == "provider":
            # user do profissional
            return conv.professional.user_id

        return conv.family_user_id

    def get_sender_professional_id(self, obj: Message):
        conv = obj.conversation
        if not conv:
            return None

        if obj.sender_role == "provider":
            # id do ProfessionalProfile (serve para link /professionals/<id>)
            return conv.professional_id

        return None


class ConversationListSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    last_message_at = serializers.SerializerMethodField()

    # (opcional, mas ajuda MUITO no frontend)
    professional_name = serializers.CharField(source="professional.display_name", read_only=True)
    family_name = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "id",
            "professional",
            "professional_name",
            "family_user",
            "family_name",
            "updated_at",
            "last_message",
            "last_message_at",
        ]

    def get_family_name(self, obj: Conversation):
        fam_profile = getattr(obj.family_user, "family_profile", None)
        return (
            getattr(fam_profile, "display_name", None)
            or getattr(obj.family_user, "email", None)
            or "Familiar"
        )

    def get_last_message(self, obj):
        m = obj.messages.last()
        return m.body if m else None

    def get_last_message_at(self, obj):
        m = obj.messages.last()
        return m.created_at if m else None