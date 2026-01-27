from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import FamilyProfile
from providers.models import ProfessionalProfile

User = get_user_model()


# ============================================================
# LEGACY: serializers que você já usa hoje (mantidos)
# ============================================================

class FamilyRegisterSerializer(serializers.Serializer):
    """
    Payload sugerido (exemplo):
    {
      "email": "...",
      "password": "...",
      "display_name": "...",
      "city": "...",
      "zipcode": "...",
      "due_date": "2026-06-01",   # opcional
      "bio": "...",              # opcional
      "photo": "https://..."     # opcional
    }
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)

    display_name = serializers.CharField()
    city = serializers.CharField(required=False, allow_blank=True)
    zipcode = serializers.CharField(required=False, allow_blank=True)
    due_date = serializers.DateField(required=False, allow_null=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    photo = serializers.URLField(required=False, allow_null=True, allow_blank=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")

        email = validated_data.pop("email")
        user = User.objects.create_user(
            email=email,
            password=password,
            role="family",
        )

        FamilyProfile.objects.create(
            user=user,
            display_name=validated_data.get("display_name", ""),
            city=validated_data.get("city", ""),
            zipcode=validated_data.get("zipcode", ""),
            due_date=validated_data.get("due_date"),
            bio=validated_data.get("bio", ""),
            photo=validated_data.get("photo"),
        )
        return user


class ProfessionalRegisterSerializer(serializers.Serializer):
    """
    Payload sugerido (exemplo):
    {
      "email": "...",
      "password": "...",
      "display_name": "...",
      "headline": "...",
      "service_types": ["...","..."],  # opcional
      "city": "...", "state": "...", "zipcode": "...",
      "bio": "...", "photo": "https://..."
    }
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)

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

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        email = validated_data.pop("email")

        user = User.objects.create_user(
            email=email,
            password=password,
            role="provider",
        )

        ProfessionalProfile.objects.create(
            user=user,
            display_name=validated_data.get("display_name", ""),
            headline=validated_data.get("headline", ""),
            service_types=validated_data.get("service_types", []),
            city=validated_data.get("city", ""),
            state=validated_data.get("state", ""),
            zipcode=validated_data.get("zipcode", ""),
            bio=validated_data.get("bio", ""),
            photo=validated_data.get("photo"),
        )
        return user


class FamilyProfileMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyProfile
        fields = ["display_name", "city", "zipcode", "due_date", "bio", "photo"]


# ============================================================
# NOVO: Signup unificado (para seu frontend novo)
# ============================================================

class SignupSerializer(serializers.Serializer):
    """
    Payload esperado:
    {
      "role": "family" | "provider",
      "user": { "email": "...", "password": "..." },
      "profile": { ...campos por role... }
    }
    """
    role = serializers.ChoiceField(choices=["family", "provider"])
    user = serializers.DictField()
    profile = serializers.DictField()

    def validate(self, attrs):
        role = attrs.get("role")
        user_data = attrs.get("user") or {}
        profile_data = attrs.get("profile") or {}

        email = user_data.get("email")
        password = user_data.get("password")

        if not email:
            raise serializers.ValidationError({"user": {"email": "This field is required."}})
        if not password:
            raise serializers.ValidationError({"user": {"password": "This field is required."}})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"user": {"email": "Email already exists."}})

        # validação mínima do profile
        if not profile_data.get("display_name"):
            raise serializers.ValidationError({"profile": {"display_name": "This field is required."}})

        # validação extra opcional por role (se quiser exigir headline)
        # if role == "provider" and not profile_data.get("headline"):
        #     raise serializers.ValidationError({"profile": {"headline": "This field is required."}})

        return attrs

    def create(self, validated_data):
        role = validated_data["role"]
        user_data = validated_data["user"]
        profile_data = validated_data["profile"]

        user = User.objects.create_user(
            email=user_data["email"],
            password=user_data["password"],
            role=role,
        )

        if role == "family":
            FamilyProfile.objects.create(
                user=user,
                display_name=profile_data.get("display_name", ""),
                city=profile_data.get("city", ""),
                zipcode=profile_data.get("zipcode", ""),
                due_date=profile_data.get("due_date"),
                bio=profile_data.get("bio", ""),
                photo=profile_data.get("photo"),
            )

        if role == "provider":
            ProfessionalProfile.objects.create(
                user=user,
                display_name=profile_data.get("display_name", ""),
                headline=profile_data.get("headline", ""),
                service_types=profile_data.get("service_types", []),
                city=profile_data.get("city", ""),
                state=profile_data.get("state", ""),
                zipcode=profile_data.get("zipcode", ""),
                bio=profile_data.get("bio", ""),
                photo=profile_data.get("photo"),
            )

        return user


# ============================================================
# NOVO: /auth/me unificado (GET/PATCH)
# ============================================================

class MeSerializer(serializers.Serializer):
    # read-only do user
    email = serializers.EmailField(read_only=True)
    role = serializers.CharField(read_only=True)

    # campos que podem ser atualizados (comuns)
    display_name = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    state = serializers.CharField(required=False, allow_blank=True)
    zipcode = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    photo = serializers.CharField(required=False, allow_blank=True)

    # provider only
    headline = serializers.CharField(required=False, allow_blank=True)
    service_types = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )

    def to_representation(self, instance):
        """
        instance = request.user
        """
        user = instance
        data = {"email": user.email, "role": user.role}

        if user.role == "family":
            if hasattr(user, "family_profile"):
                p = user.family_profile
                data.update({
                    "display_name": p.display_name,
                    "city": p.city,
                    "zipcode": p.zipcode,
                    "bio": p.bio,
                    "photo": p.photo or "",
                })

        if user.role == "provider":
            if hasattr(user, "professional_profile"):
                p = user.professional_profile
                data.update({
                    "display_name": p.display_name,
                    "headline": p.headline,
                    "service_types": p.service_types or [],
                    "city": p.city,
                    "state": p.state,
                    "zipcode": p.zipcode,
                    "bio": p.bio,
                    "photo": p.photo or "",
                })

        return data

    def update(self, instance, validated_data):
        """
        instance = request.user
        """
        user = instance

        if user.role == "family":
            if not hasattr(user, "family_profile"):
                raise serializers.ValidationError({"detail": "Not a family user."})

            p = user.family_profile
            for field in ["display_name", "city", "zipcode", "bio", "photo"]:
                if field in validated_data:
                    setattr(p, field, validated_data[field])
            p.save()
            return user

        if user.role == "provider":
            if not hasattr(user, "professional_profile"):
                raise serializers.ValidationError({"detail": "Not a provider user."})

            p = user.professional_profile
            for field in ["display_name", "headline", "service_types", "city", "state", "zipcode", "bio", "photo"]:
                if field in validated_data:
                    setattr(p, field, validated_data[field])
            p.save()
            return user

        raise serializers.ValidationError({"detail": "Invalid role."})
