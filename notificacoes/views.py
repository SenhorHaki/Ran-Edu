# Em notificacoes/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notificacao
from .serializers import NotificacaoSerializer

class NotificacaoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para visualizar e interagir com as notificações.
    'ReadOnly' significa que ele só permite listar e ver detalhes, não criar/apagar via API.
    """
    serializer_class = NotificacaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filtra para retornar apenas as notificações do destinatário
        que fez a requisição.
        """
        return Notificacao.objects.filter(destinatario=self.request.user)

    @action(detail=True, methods=['post'])
    def marcar_como_lida(self, request, pk=None):
        """
        Ação customizada para marcar uma notificação específica como lida.
        Ex: POST /api/notificacoes/5/marcar_como_lida/
        """
        notificacao = self.get_object() # Pega a notificação pelo ID da URL
        notificacao.lida = True
        notificacao.save()
        return Response({'status': 'notificação marcada como lida'})
    
