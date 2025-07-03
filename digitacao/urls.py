from rest_framework.routers import DefaultRouter
from .views import LicaoDigitacaoViewSet, ResultadoDigitacaoViewSet

router = DefaultRouter()
router.register(r'licoes', LicaoDigitacaoViewSet, basename='licao-digitacao')
router.register(r'resultados', ResultadoDigitacaoViewSet, basename='resultado-digitacao')

urlpatterns = router.urls