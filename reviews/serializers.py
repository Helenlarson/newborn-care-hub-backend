from rest_framework import serializers
from .models import Review
from providers.models import ProfessionalProfile

class ReviewCreateSerializer(serializers.ModelSerializer):
    professional_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = ["professional_id", "rating", "comment", "created_at"]
        read_only_fields = ["created_at"]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        professional_id = validated_data.pop("professional_id")
        professional = ProfessionalProfile.objects.get(id=professional_id)

        user = self.context["request"].user

        # regra: só família pode criar review
        if not hasattr(user, "family_profile"):
            raise serializers.ValidationError("Only family users can create reviews.")

        return Review.objects.create(
            professional=professional,
            family_user=user,
            **validated_data
        )
