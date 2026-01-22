from django.contrib.auth.models import User
from rest_framework import serializers
from accounts.models import FamilyProfile
from providers.models import ProfessionalProfile, ServiceType


class FamilyRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    display_name = serializers.CharField(max_length=120)
    city = serializers.CharField(max_length=80)
    zipcode = serializers.CharField(max_length=10)
    due_date = serializers.DateField(required=False, allow_null=True)
    bio = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        email = validated_data["email"].lower()
        password = validated_data["password"]

        user = User.objects.create_user(username=email, email=email, password=password)

        FamilyProfile.objects.create(
            user=user,
            display_name=validated_data["display_name"],
            city=validated_data["city"],
            zipcode=validated_data["zipcode"],
            due_date=validated_data.get("due_date"),
            bio=validated_data.get("bio", ""),
        )
        return user


class ProfessionalRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    display_name = serializers.CharField(max_length=120)
    city = serializers.CharField(max_length=80)
    zipcode = serializers.CharField(max_length=10)
    bio = serializers.CharField(required=False, allow_blank=True)
    experience_years = serializers.IntegerField(min_value=0, required=False)

    # lista de slugs: ["birth-doula","postpartum-doula"]
    service_type_slugs = serializers.ListField(
        child=serializers.SlugField(),
        allow_empty=True,
        required=False
    )

    def create(self, validated_data):
        email = validated_data["email"].lower()
        password = validated_data["password"]

        user = User.objects.create_user(username=email, email=email, password=password)

        profile = ProfessionalProfile.objects.create(
            user=user,
            display_name=validated_data["display_name"],
            city=validated_data["city"],
            zipcode=validated_data["zipcode"],
            bio=validated_data.get("bio", ""),
            experience_years=validated_data.get("experience_years", 0),
        )

        slugs = validated_data.get("service_type_slugs", [])
        if slugs:
            services = ServiceType.objects.filter(slug__in=slugs)
            profile.service_types.set(services)

        return user
    

class FamilyProfileMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyProfile
        fields = ["display_name", "city", "zipcode", "due_date", "bio", "photo"]

