from rest_framework import serializers
from .models import ProfessionalProfile, ServiceType

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ["id", "name", "slug"]

class ProfessionalProfileListSerializer(serializers.ModelSerializer):
    service_types = ServiceTypeSerializer(many=True, read_only=True)

    class Meta:
        model = ProfessionalProfile
        fields = ["id", "display_name", "city", "zipcode", "bio", "experience_years", "service_types", "photo"]

class ProfessionalProfileMeUpdateSerializer(serializers.ModelSerializer):
    # permitir atualizar via IDs
    service_type_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = ProfessionalProfile
        fields = ["display_name", "city", "zipcode", "bio", "experience_years", "photo", "service_type_ids"]

    def update(self, instance, validated_data):
        ids = validated_data.pop("service_type_ids", None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()

        if ids is not None:
            services = ServiceType.objects.filter(id__in=ids)
            instance.service_types.set(services)

        return instance
