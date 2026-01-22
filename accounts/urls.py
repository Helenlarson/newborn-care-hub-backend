from django.urls import path
from .views import RegisterFamilyView, RegisterProfessionalView, FamilyMeView

urlpatterns = [
    path("auth/register/family/", RegisterFamilyView.as_view()),
    path("auth/register/professional/", RegisterProfessionalView.as_view()),
    path("family/me/", FamilyMeView.as_view()),
]
