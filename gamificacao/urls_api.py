from django.urls import path
from .views import MinhasConquistasView 

urlpatterns = [
    path('minhas-conquistas/', MinhasConquistasView.as_view(), name='minhas-conquistas-api'),
]