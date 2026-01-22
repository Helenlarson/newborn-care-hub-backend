from django.urls import path
from .views import ProfessionalListView, ProfessionalDetailView, ProfessionalMeView, ServiceTypeListView

urlpatterns = [
    path("service-types/", ServiceTypeListView.as_view()),
    path("professionals/", ProfessionalListView.as_view()),
    path("professionals/<int:pk>/", ProfessionalDetailView.as_view()),
    path("professionals/me/", ProfessionalMeView.as_view()),
]
