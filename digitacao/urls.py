from django.urls import path
from .views import GameView

app_name = 'digitacao'

urlpatterns = [
    path('game/', GameView.as_view(), name='game-page'),
]