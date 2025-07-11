from django.urls import path, include
from .views import CriarUsuarioView, MeView, LoginView, LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'usuarios'

api_urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', CriarUsuarioView.as_view(), name='register'),
    path('me/', MeView.as_view(), name='me'),
]

web_urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

urlpatterns = [
    path('api/', include(api_urlpatterns)),
    path('', include(web_urlpatterns)),
]