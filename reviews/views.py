from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Review
from .serializers import ReviewCreateSerializer

class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReviewListByProfessionalView(generics.ListAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        prof_id = self.kwargs["professional_id"]
        return Review.objects.filter(professional_id=prof_id)
