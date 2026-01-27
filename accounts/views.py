from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .serializers import (
    FamilyRegisterSerializer,
    ProfessionalRegisterSerializer,
    FamilyProfileMeSerializer,
    SignupSerializer,
    MeSerializer,
)


# ============================================================
# LEGACY ENDPOINTS (mantidos para compatibilidade)
# ============================================================

class RegisterFamilyView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = FamilyRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": "Family user created.",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role,
                },
            },
            status=status.HTTP_201_CREATED
        )


class RegisterProfessionalView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ProfessionalRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": "Professional user created.",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role,
                },
            },
            status=status.HTTP_201_CREATED
        )


# ============================================================
# NOVO ENDPOINT UNIFICADO
# POST /auth/signup
# ============================================================

class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Payload esperado:
        {
          "role": "family" | "provider",
          "user": { "email": "...", "password": "..." },
          "profile": { ... }
        }
        """
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "message": "User created successfully",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role,
                },
            },
            status=status.HTTP_201_CREATED
        )


# ============================================================
# /auth/me (unificado)
# GET / PATCH
# ============================================================

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = MeSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = MeSerializer(
            instance=request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(MeSerializer(user).data)


# ============================================================
# ENDPOINT ANTIGO (family-only)
# Mantido para não quebrar fluxos antigos
# ============================================================

class FamilyMeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, "family_profile"):
            return Response(
                {"detail": "Not a family user."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = FamilyProfileMeSerializer(request.user.family_profile)
        return Response(serializer.data)

    def patch(self, request):
        if not hasattr(request.user, "family_profile"):
            return Response(
                {"detail": "Not a family user."},
                status=status.HTTP_403_FORBIDDEN
            )
        profile = request.user.family_profile
        serializer = FamilyProfileMeSerializer(
            profile,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
