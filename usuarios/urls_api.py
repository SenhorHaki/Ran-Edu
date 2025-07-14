from django.urls import path
from .views import CriarUsuarioView, MeView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', CriarUsuarioView.as_view(), name='register-api'),
    path('me/', MeView.as_view(), name='me-api'),
]