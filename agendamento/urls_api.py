from django.urls import path
from .views import AgendaViewAPI

urlpatterns = [
    path('minha-agenda/', AgendaViewAPI.as_view(), name='minha-agenda-api'),
]