from rest_framework import serializers
from .models import Message
from providers.models import ProfessionalProfile

class MessageCreateSerializer(serializers.ModelSerializer):
    professional_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Message
        fields = ["professional_id", "family_name", "family_email", "family_city", "family_zipcode", "message", "created_at"]
        read_only_fields = ["created_at"]

    def create(self, validated_data):
        professional_id = validated_data.pop("professional_id")
        professional = ProfessionalProfile.objects.get(id=professional_id)
        return Message.objects.create(professional=professional, **validated_data)

class MessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "family_name", "family_email", "family_city", "family_zipcode", "message", "created_at"]
