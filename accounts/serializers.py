# accounts/serializers.py
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from .models import FamilyProfile, ProfessionalProfile, ServiceType

User = get_user_model()


# ----------------------------
# Models serializers (usados pelas views)
# ----------------------------

class FamilyProfileMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyProfile
        fields = ["display_name", "city", "zipcode", "due_date", "bio", "photo"]


class ProfessionalProfileListSerializer(serializers.ModelSerializer):
    service_types = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )

    class Meta:
        model = ProfessionalProfile
        fields = [
            "id",
            "display_name",
            "headline",
            "service_types",
            "city",
            "state",
            "zipcode",
            "bio",
            "photo",
        ]


class ProfessionalProfileMeUpdateSerializer(serializers.ModelSerializer):
    service_types = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )

    class Meta:
        model = ProfessionalProfile
        fields = [
            "display_name",
            "headline",
            "service_types",
            "city",
            "state",
            "zipcode",
            "bio",
            "photo",
        ]


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ["id", "name", "slug"]


# ----------------------------
# Signup unificado (cria user + profile)
# ----------------------------

class _SignupUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)


class _FamilyProfileCreateSerializer(serializers.Serializer):
    display_name = serializers.CharField()
    city = serializers.CharField(required=False, allow_blank=True)
    zipcode = serializers.CharField(required=False, allow_blank=True)
    due_date = serializers.DateField(required=False, allow_null=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    photo = serializers.URLField(required=False, allow_null=True, allow_blank=True)


class _ProfessionalProfileCreateSerializer(serializers.Serializer):
    display_name = serializers.CharField()
    headline = serializers.CharField(required=False, allow_blank=True)
    service_types = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    city = serializers.CharField(required=False, allow_blank=True)
    state = serializers.CharField(required=False, allow_blank=True)
    zipcode = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    photo = serializers.URLField(required=False, allow_null=True, allow_blank=True)


class SignupSerializer(serializers.Serializer):
    """
    Payload:
    {
      "role": "family" | "provider",
      "user": { "email": "...", "password": "..." },
      "profile": { ... }
    }
    """
    role = serializers.ChoiceField(choices=["family", "provider"])
    user = _SignupUserSerializer()
    profile = serializers.DictField()

    def validate(self, attrs):
        role = attrs["role"]
        user_data = attrs["user"]
        profile_data = attrs["profile"] or {}

        email = user_data.get("email")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"user": {"email": "Email already exists."}})

        # valida profile de acordo com role
        if role == "family":
            p = _FamilyProfileCreateSerializer(data=profile_data)
        else:
            p = _ProfessionalProfileCreateSerializer(data=profile_data)

        p.is_valid(raise_exception=True)
        attrs["_profile_validated"] = p.validated_data
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        role = validated_data["role"]
        user_data = validated_data["user"]
        profile_data = validated_data["_profile_validated"]

        user = User.objects.create_user(
            email=user_data["email"],
            password=user_data["password"],
            role=role,
        )

        if role == "family":
            FamilyProfile.objects.create(user=user, **profile_data)
        else:
            # garante default pra lista
            profile_data.setdefault("service_types", [])
            ProfessionalProfile.objects.create(user=user, **profile_data)

        return user


# ----------------------------
# /auth/me unificado (GET/PATCH)
# ----------------------------

class MeSerializer(serializers.Serializer):
    # read-only
    email = serializers.EmailField(read_only=True)
    role = serializers.CharField(read_only=True)

    # campos comuns
    display_name = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    state = serializers.CharField(required=False, allow_blank=True)
    zipcode = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    photo = serializers.URLField(required=False, allow_null=True, allow_blank=True)

    # family only
    due_date = serializers.DateField(required=False, allow_null=True)

    # provider only
    headline = serializers.CharField(required=False, allow_blank=True)
    service_types = serializers.ListField(child=serializers.CharField(), required=False)

    def to_representation(self, instance):
        user = instance
        data = {"email": user.email, "role": user.role}

        if user.role == "family" and hasattr(user, "family_profile"):
            p = user.family_profile
            data.update({
                "display_name": p.display_name,
                "city": p.city,
                "zipcode": p.zipcode,
                "due_date": p.due_date,
                "bio": p.bio,
                "photo": p.photo,
            })

        if user.role == "provider" and hasattr(user, "professional_profile"):
            p = user.professional_profile
            data.update({
                "display_name": p.display_name,
                "headline": p.headline,
                "service_types": p.service_types or [],
                "city": p.city,
                "state": p.state,
                "zipcode": p.zipcode,
                "bio": p.bio,
                "photo": p.photo,
            })

        return data

    def update(self, instance, validated_data):
        user = instance

        if user.role == "family":
            if not hasattr(user, "family_profile"):
                raise serializers.ValidationError({"detail": "Not a family user."})
            p = user.family_profile
            for f in ["display_name", "city", "zipcode", "due_date", "bio", "photo"]:
                if f in validated_data:
                    setattr(p, f, validated_data[f])
            p.save()
            return user

        if user.role == "provider":
            if not hasattr(user, "professional_profile"):
                raise serializers.ValidationError({"detail": "Not a provider user."})
            p = user.professional_profile
            for f in ["display_name", "headline", "service_types", "city", "state", "zipcode", "bio", "photo"]:
                if f in validated_data:
                    setattr(p, f, validated_data[f])
            p.save()
            return user

        raise serializers.ValidationError({"detail": "Invalid role."})
