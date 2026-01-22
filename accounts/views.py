from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import FamilyRegisterSerializer, ProfessionalRegisterSerializer, FamilyProfileMeSerializer

class RegisterFamilyView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = FamilyRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Family user created."}, status=status.HTTP_201_CREATED)

class RegisterProfessionalView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ProfessionalRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Professional user created."}, status=status.HTTP_201_CREATED)

class FamilyMeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, "family_profile"):
            return Response({"detail": "Not a family user."}, status=403)
        ser = FamilyProfileMeSerializer(request.user.family_profile)
        return Response(ser.data)

    def patch(self, request):
        if not hasattr(request.user, "family_profile"):
            return Response({"detail": "Not a family user."}, status=403)
        profile = request.user.family_profile
        ser = FamilyProfileMeSerializer(profile, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)
