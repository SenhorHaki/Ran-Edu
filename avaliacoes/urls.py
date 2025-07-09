# Em avaliacoes/urls.py
from django.urls import path
from .views import BoletimView

app_name = 'avaliacoes'

urlpatterns = [
    path('boletim/', BoletimView.as_view(), name='boletim-web'),
]