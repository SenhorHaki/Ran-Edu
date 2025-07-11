from django.urls import path
from .views import ListaConquistasView

app_name = 'gamificacao'

urlpatterns = [
    path('conquistas/', ListaConquistasView.as_view(), name='lista-conquistas'),
]