from rest_framework import serializers
from .models import Conversation, Message


class ContactCreateSerializer(serializers.Serializer):
    professional_id = serializers.IntegerField()
    message = serializers.CharField()


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "sender_role", "body", "created_at", "is_read"]


class ConversationListSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    last_message_at = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ["id", "professional", "family_user", "updated_at", "last_message", "last_message_at"]

    def get_last_message(self, obj):
        m = obj.messages.last()
        return m.body if m else None

    def get_last_message_at(self, obj):
        m = obj.messages.last()
        return m.created_at if m else None
