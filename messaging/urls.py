from django.urls import path
from .views import MessageCreateView, ProfessionalInboxView

urlpatterns = [
    path("contact/", MessageCreateView.as_view()),
    path("inbox/", ProfessionalInboxView.as_view()),
]
