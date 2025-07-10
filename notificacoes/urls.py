from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificacaoViewSet, PainelAlertasView, MarcarAlertaComoLidoView

app_name = 'notificacoes'

router = DefaultRouter()
router.register(r'api', NotificacaoViewSet, basename='notificacao-api')

urlpatterns = [
    path('', PainelAlertasView.as_view(), name='painel-alertas'),
    path('<int:pk>/marcar-como-lida/', MarcarAlertaComoLidoView.as_view(), name='marcar-como-lida'),
]

urlpatterns += router.urls