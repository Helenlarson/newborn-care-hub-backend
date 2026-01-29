from django.urls import path
from .views import MessageCreateView, ProfessionalInboxView, FamilyInboxView, ConversationMessagesView

urlpatterns = [
    path("contact/", MessageCreateView.as_view()),
    path("inbox/", ProfessionalInboxView.as_view()),
    path("family/inbox/", FamilyInboxView.as_view()),
    path("conversations/<int:conversation_id>/messages/", ConversationMessagesView.as_view()),
]
