from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import LicaoDigitacaoViewSet, ResultadoDigitacaoViewSet, GameView 

app_name = 'digitacao'






router = DefaultRouter()
router.register(r'licoes', LicaoDigitacaoViewSet, basename='licao-digitacao')
router.register(r'resultados', ResultadoDigitacaoViewSet, basename='resultado-digitacao')

urlpatterns = [
    path('api/', include(router.urls)),
    path('game/', GameView.as_view(), name='game-page'),
    
]
