from rest_framework import generics, permissions
from .models import Notificacao
from .serializers import NotificacaoSerializer

class MinhasNotificacoesView(generics.ListAPIView):
    """
    View para listar todas as notificações do usuário logado.
    """
    serializer_class = NotificacaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filtra o queryset para retornar apenas as notificações do destinatário
        que fez a requisição.
        """
        return Notificacao.objects.filter(destinatario=self.request.user)