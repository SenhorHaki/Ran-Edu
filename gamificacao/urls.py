

from django.urls import path
from .views import MinhasConquistasView, ListaConquistasView

app_name = 'gamificacao'

urlpatterns = [
    path('conquistas/', ListaConquistasView.as_view(), name='lista-conquistas'),
    
    path('api/minhas-conquistas/', MinhasConquistasView.as_view(), name='minhas-conquistas-api'),
]