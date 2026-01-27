from django.urls import path
from .views import (
    RegisterFamilyView,
    RegisterProfessionalView,
    SignupView,
    MeView,
    FamilyMeView,
)

urlpatterns = [
    path("register/family", RegisterFamilyView.as_view()),
    path("register/professional", RegisterProfessionalView.as_view()),
    path("signup", SignupView.as_view()),
    path("me", MeView.as_view()),
    path("me/family", FamilyMeView.as_view()),
]
