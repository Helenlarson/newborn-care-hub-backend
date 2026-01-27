from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),

    # AUTH
    path("api/auth/", include("accounts.urls")),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # API
    path("api/", include("providers.urls")),
    path("api/", include("reviews.urls")),
    path("api/", include("messaging.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
