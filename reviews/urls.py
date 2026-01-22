from django.urls import path
from .views import ReviewCreateView, ReviewListByProfessionalView

urlpatterns = [
    path("reviews/", ReviewCreateView.as_view()),
    path("professionals/<int:professional_id>/reviews/", ReviewListByProfessionalView.as_view()),
]
