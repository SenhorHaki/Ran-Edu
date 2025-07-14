from rest_framework.routers import DefaultRouter
from .views import RecursoViewSet

router = DefaultRouter()
router.register(r'recursos', RecursoViewSet, basename='recurso-api')

urlpatterns = router.urls