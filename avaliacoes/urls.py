from django.urls import path
from .views import MeuBoletimView

urlpatterns = [
    # Define a rota para a nossa view de boletim
    path('meu-boletim/', MeuBoletimView.as_view(), name='meu-boletim'),
]