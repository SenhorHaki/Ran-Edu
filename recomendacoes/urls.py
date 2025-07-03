from django.urls import path
from .views import RecomendacaoListView

urlpatterns = [
    path('', RecomendacaoListView.as_view(), name='lista-recomendacoes'),
]
