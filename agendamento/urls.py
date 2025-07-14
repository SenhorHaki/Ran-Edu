# Em agendamento/urls.py
from django.urls import path
from .views import AgendaView

app_name = 'agendamento'

urlpatterns = [
    path('minha-agenda/', AgendaView.as_view(), name='minha-agenda'),
]