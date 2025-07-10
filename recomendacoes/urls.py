from django.urls import path
from .views import RecomendacaoView

app_name = 'recomendacoes'

urlpatterns = [
    path('', RecomendacaoView.as_view(), name='lista-recomendacoes'),
]