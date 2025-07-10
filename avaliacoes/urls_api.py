# Em avaliacoes/urls_api.py
from django.urls import path
from .views import MeuBoletimView

urlpatterns = [
    path('meu-boletim/', MeuBoletimView.as_view(), name='meu-boletim-api'),
]