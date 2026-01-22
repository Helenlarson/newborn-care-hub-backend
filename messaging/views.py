from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Message
from .serializers import MessageCreateSerializer, MessageListSerializer

class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageCreateSerializer
    permission_classes = [permissions.AllowAny]  # família pode não estar logada

class ProfessionalInboxView(generics.ListAPIView):
    serializer_class = MessageListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # só profissional enxerga inbox dele
        return Message.objects.filter(professional=self.request.user.professional_profile)
