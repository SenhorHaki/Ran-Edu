# cursos/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CursoViewSet,
    ModuloViewSet,
    AulaViewSet,
    MinhasInscricoesView,
    PostagemViewSet,
    ComentarioViewSet
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
]