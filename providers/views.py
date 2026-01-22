from django.shortcuts import render
# Create your views here.
from rest_framework import generics, permissions
from django_filters.rest_framework import FilterSet, filters
from .models import ProfessionalProfile, ServiceType
from .serializers import ProfessionalProfileListSerializer, ProfessionalProfileMeUpdateSerializer, ServiceTypeSerializer

class ProfessionalFilter(FilterSet):
    city = filters.CharFilter(field_name="city", lookup_expr="icontains")
    zipcode = filters.CharFilter(field_name="zipcode", lookup_expr="exact")
    service_type = filters.CharFilter(field_name="service_types__slug", lookup_expr="exact")

    class Meta:
        model = ProfessionalProfile
        fields = ["city", "zipcode", "service_type"]

class ProfessionalListView(generics.ListAPIView):
    queryset = ProfessionalProfile.objects.all().prefetch_related("service_types")
    serializer_class = ProfessionalProfileListSerializer
    permission_classes = [permissions.AllowAny]
    filterset_class = ProfessionalFilter
    search_fields = ["display_name", "bio", "city"]

class ProfessionalDetailView(generics.RetrieveAPIView):
    queryset = ProfessionalProfile.objects.all().prefetch_related("service_types")
    serializer_class = ProfessionalProfileListSerializer
    permission_classes = [permissions.AllowAny]

class ProfessionalMeView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfessionalProfileMeUpdateSerializer

    def get_object(self):
        return self.request.user.professional_profile

class ServiceTypeListView(generics.ListAPIView):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [permissions.AllowAny]
