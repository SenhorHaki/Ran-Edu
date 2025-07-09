from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AvaliacaoViewSet, NotaViewSet, MeuBoletimView

router = DefaultRouter()
router.register(r'avaliacoes', AvaliacaoViewSet, basename='avaliacao')
router.register(r'notas', NotaViewSet, basename='nota')

urlpatterns = [
    path('', include(router.urls)),
    path('meu-boletim/', MeuBoletimView.as_view(), name='meu-boletim-api'),
]