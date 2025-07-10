from django.urls import path
from .views import BibliotecaView

app_name = 'biblioteca'

urlpatterns = [
    path('', BibliotecaView.as_view(), name='lista-recursos'),
]