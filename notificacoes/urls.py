from django.urls import path
from .views import PainelAlertasView, MarcarAlertaComoLidoView

app_name = 'notificacoes'

urlpatterns = [
    path('', PainelAlertasView.as_view(), name='painel-alertas'),
    path('<int:pk>/marcar-como-lida/', MarcarAlertaComoLidoView.as_view(), name='marcar-como-lida'),
]