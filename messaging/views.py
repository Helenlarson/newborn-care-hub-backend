from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import NotFound, PermissionDenied

from accounts.models import ProfessionalProfile
from .models import Conversation, Message
from .serializers import (
    ContactCreateSerializer,
    ConversationListSerializer,
    MessageSerializer,
)


class MessageCreateView(APIView):
    """
    POST /api/contact/
    Cria (ou encontra) a Conversation e registra a primeira mensagem (family -> provider)
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user.role != "family":
            raise PermissionDenied("Only family users can send messages.")

        ser = ContactCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        professional_id = ser.validated_data["professional_id"]
        text = ser.validated_data["message"]

        try:
            professional = ProfessionalProfile.objects.get(id=professional_id)
        except ProfessionalProfile.DoesNotExist:
            raise NotFound("Professional not found.")

        conv, _ = Conversation.objects.get_or_create(
            professional=professional,
            family_user=request.user
        )

        msg = Message.objects.create(
            conversation=conv,
            sender_role="family",
            body=text
        )

        return Response(
            {"conversation_id": conv.id, "message": MessageSerializer(msg).data},
            status=status.HTTP_201_CREATED
        )


class ProfessionalInboxView(ListAPIView):
    """
    GET /api/inbox/
    Lista conversas do profissional logado
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConversationListSerializer

    def get_queryset(self):
        if self.request.user.role != "provider":
            raise PermissionDenied("Only providers can access this inbox.")

        try:
            prof = self.request.user.professional_profile
        except ProfessionalProfile.DoesNotExist:
            raise NotFound("Professional profile not found.")

        return (
            Conversation.objects
            .filter(professional=prof)
            .select_related("professional", "family_user", "family_user__family_profile")
            .prefetch_related("messages")
        )


class FamilyInboxView(ListAPIView):
    """
    GET /api/family/inbox/
    Lista conversas da família logada
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConversationListSerializer

    def get_queryset(self):
        if self.request.user.role != "family":
            raise PermissionDenied("Only family users can access this inbox.")

        return (
            Conversation.objects
            .filter(family_user=self.request.user)
            .select_related("professional", "family_user", "family_user__family_profile")
            .prefetch_related("messages")
        )


class ConversationMessagesView(APIView):
    """
    GET /api/conversations/<id>/messages/  -> lista mensagens
    POST /api/conversations/<id>/messages/ -> envia mensagem (family ou provider)
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_conversation(self, conversation_id, user):
        try:
            conv = (
                Conversation.objects
                .select_related(
                    "professional",
                    "professional__user",
                    "family_user",
                    "family_user__family_profile",
                )
                .get(id=conversation_id)
            )
        except Conversation.DoesNotExist:
            raise NotFound("Conversation not found.")

        prof_profile_id = None
        if user.role == "provider":
            try:
                prof_profile_id = user.professional_profile.id
            except ProfessionalProfile.DoesNotExist:
                prof_profile_id = None

        is_provider = (user.role == "provider" and prof_profile_id and conv.professional_id == prof_profile_id)
        is_family = (user.role == "family" and conv.family_user_id == user.id)

        if not (is_provider or is_family):
            raise PermissionDenied("You are not a participant of this conversation.")

        return conv

    def get(self, request, conversation_id):
        conv = self.get_conversation(conversation_id, request.user)

        msgs = (
            Message.objects
            .filter(conversation=conv)
            .select_related(
                "conversation",
                "conversation__professional",
                "conversation__professional__user",
                "conversation__family_user",
                "conversation__family_user__family_profile",
            )
            .order_by("created_at")
        )

        return Response(MessageSerializer(msgs, many=True).data)

    def post(self, request, conversation_id):
        conv = self.get_conversation(conversation_id, request.user)

        text = request.data.get("message") or request.data.get("body")
        if not text:
            return Response({"message": "This field is required."}, status=400)

        sender_role = request.user.role  # "family" ou "provider"

        msg = Message.objects.create(
            conversation=conv,
            sender_role=sender_role,
            body=text
        )

        conv.save(update_fields=["updated_at"])

        # recarrega com select_related para o serializer ter acesso aos nomes sem query extra
        msg = (
            Message.objects
            .select_related(
                "conversation",
                "conversation__professional",
                "conversation__professional__user",
                "conversation__family_user",
                "conversation__family_user__family_profile",
            )
            .get(pk=msg.pk)
        )

        return Response(MessageSerializer(msg).data, status=status.HTTP_201_CREATED)
