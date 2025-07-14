from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CursoViewSet,
    ModuloViewSet,
    AulaViewSet,
    MinhasInscricoesView,
    PostagemViewSet,
    ComentarioViewSet,
    GerarCertificadoView,
    ForunsDisponiveisView,
    SelecaoForumView,
    ListaPostagensView 
)


router = DefaultRouter()
router.register(r'cursos', CursoViewSet, basename='curso')
router.register(r'modulos', ModuloViewSet, basename='modulo')
router.register(r'aulas', AulaViewSet, basename='aula')
router.register(r'postagens', PostagemViewSet, basename='postagem')
router.register(r'comentarios', ComentarioViewSet, basename='comentario')

urlpatterns = [
    path('', include(router.urls)),    
    path('meus-cursos/', MinhasInscricoesView.as_view(), name='meus-cursos'),
    path('inscricoes/<int:inscricao_id>/gerar-certificado/', GerarCertificadoView.as_view(), name='gerar-certificado'),
    path('foruns-disponiveis/', ForunsDisponiveisView.as_view(), name='foruns-disponiveis'),
    path('selecao-forum/', SelecaoForumView.as_view(), name='selecao-forum'),
    path('forum/', ListaPostagensView.as_view(), name='lista-postagens'),
    
]