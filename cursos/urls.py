from django.urls import path
from .views import SelecaoForumView, ListaPostagensView

app_name = 'cursos'

urlpatterns = [
    path('selecao-forum/', SelecaoForumView.as_view(), name='selecao-forum'),
    path('forum/', ListaPostagensView.as_view(), name='lista-postagens'),
]