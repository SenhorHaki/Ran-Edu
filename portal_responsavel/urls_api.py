from django.urls import path
from .views import PortalResponsavelView  # Garanta que a PortalResponsavelView existe em views.py

urlpatterns = [
    path('meus-alunos/', PortalResponsavelView.as_view(), name='portal-meus-alunos-api'),
]