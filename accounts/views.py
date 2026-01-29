# accounts/views.py
from django_filters.rest_framework import FilterSet, filters, DjangoFilterBackend
from rest_framework import generics, permissions, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

from .models import ProfessionalProfile, FamilyProfile, ServiceType
from .serializers import (
    FamilyProfileMeSerializer,
    SignupSerializer,
    MeSerializer,
    ProfessionalProfileListSerializer,
    ProfessionalProfileMeUpdateSerializer,
    ServiceTypeSerializer,
)

# ============================================================
# POST /auth/signup
# cria user + profile conforme role
# ============================================================
class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
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
            status=status.HTTP_201_CREATED,
        )


# ============================================================
# /auth/me
# GET / PATCH
# ============================================================
class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(MeSerializer(request.user).data)

    def patch(self, request):
        serializer = MeSerializer(instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(MeSerializer(user).data)


# ============================================================
# /family/me (legado)
# GET / PATCH
# ============================================================
class FamilyMeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != "family":
            return Response({"detail": "Not a family user."}, status=status.HTTP_403_FORBIDDEN)
        try:
            profile = request.user.family_profile
        except FamilyProfile.DoesNotExist:
            raise NotFound("Family profile not found.")
        return Response(FamilyProfileMeSerializer(profile).data)

    def patch(self, request):
        if request.user.role != "family":
            return Response({"detail": "Not a family user."}, status=status.HTTP_403_FORBIDDEN)
        try:
            profile = request.user.family_profile
        except FamilyProfile.DoesNotExist:
            raise NotFound("Family profile not found.")

        serializer = FamilyProfileMeSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# ============================================================
# Professionals listing + filters
# Assumindo ProfessionalProfile.service_types = ["doula", "sleep-consultant", ...]
# ============================================================
class ProfessionalFilter(FilterSet):
    city = filters.CharFilter(field_name="city", lookup_expr="icontains")
    zipcode = filters.CharFilter(field_name="zipcode", lookup_expr="exact")
    service_type = filters.CharFilter(method="filter_service_type")

    def filter_service_type(self, qs, name, value):
        # JSONField list: filtra se contém o slug informado
        return qs.filter(service_types__contains=[value])

    class Meta:
        model = ProfessionalProfile
        fields = ["city", "zipcode", "service_type"]


class ProfessionalListView(generics.ListAPIView):
    queryset = ProfessionalProfile.objects.all()
    serializer_class = ProfessionalProfileListSerializer
    permission_classes = [permissions.AllowAny]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProfessionalFilter
    search_fields = ["display_name", "bio", "city", "state"]


class ProfessionalDetailView(generics.RetrieveAPIView):
    queryset = ProfessionalProfile.objects.all()
    serializer_class = ProfessionalProfileListSerializer
    permission_classes = [permissions.AllowAny]


class ProfessionalMeView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfessionalProfileMeUpdateSerializer

    def get_object(self):
        if self.request.user.role != "provider":
            raise NotFound("Professional profile not available for this user.")
        try:
            return self.request.user.professional_profile
        except ProfessionalProfile.DoesNotExist:
            raise NotFound("Professional profile not found.")


class ServiceTypeListView(generics.ListAPIView):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [permissions.AllowAny]
