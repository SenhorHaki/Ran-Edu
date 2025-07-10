from django.urls import path
from .views import (
    SelecaoForumView, 
    ListaPostagensView, 
    ListaCertificadosView, 
    GerarCertificadoView 
)

app_name = 'cursos'

urlpatterns = [
    path('selecao-forum/', SelecaoForumView.as_view(), name='selecao-forum'),
    path('forum/', ListaPostagensView.as_view(), name='lista-postagens'),
    path('certificados/', ListaCertificadosView.as_view(), name='lista-certificados'),
    path('inscricoes/<int:inscricao_id>/gerar-certificado/', GerarCertificadoView.as_view(), name='gerar-certificado'),
]