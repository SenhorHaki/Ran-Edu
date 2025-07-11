# Em gamificacao/urls_api.py
from django.urls import path
from .views import MinhasConquistasView # Nome correto da View

urlpatterns = [
    # Como não é um ViewSet, definimos a rota diretamente
    path('minhas-conquistas/', MinhasConquistasView.as_view(), name='minhas-conquistas-api'),
]