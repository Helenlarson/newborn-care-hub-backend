# accounts/urls.py
from django.urls import path
from .views import (
    SignupView, MeView, FamilyMeView,
    ProfessionalListView, ProfessionalDetailView, ProfessionalMeView,
    ServiceTypeListView,
)

urlpatterns = [
    path("auth/signup/", SignupView.as_view(), name="auth-signup"),
    path("auth/me/", MeView.as_view(), name="auth-me"),

    path("family/me/", FamilyMeView.as_view(), name="family-me"),

    path("professionals/", ProfessionalListView.as_view(), name="professionals-list"),
    path("professionals/<int:pk>/", ProfessionalDetailView.as_view(), name="professionals-detail"),
    path("professionals/me/", ProfessionalMeView.as_view(), name="professionals-me"),

    path("service-types/", ServiceTypeListView.as_view(), name="service-types-list"),
]
