from django.urls import path
from .views import RecomendacaoListViewAPI

urlpatterns = [
    path('', RecomendacaoListViewAPI.as_view(), name='lista-recomendacoes-api'),
]