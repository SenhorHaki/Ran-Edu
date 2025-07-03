from django.urls import path
from .views import AgendaView

urlpatterns = [
    path('minha-agenda/', AgendaView.as_view(), name='minha-agenda'),
]