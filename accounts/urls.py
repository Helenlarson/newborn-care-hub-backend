from django.urls import path
from .views import (
    RegisterFamilyView,
    RegisterProfessionalView,
    SignupView,
    MeView,
    FamilyMeView,
)

urlpatterns = [
    # legacy (mantidos)
    path("register/family/", RegisterFamilyView.as_view()),
    path("register/professional/", RegisterProfessionalView.as_view()),

    # novos endpoints (frontend novo usa estes)
    path("signup/", SignupView.as_view()),
    path("me/", MeView.as_view()),
    

    # legacy family-only
    path("me/family/", FamilyMeView.as_view()),
]
