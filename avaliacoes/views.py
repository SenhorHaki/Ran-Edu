# Em avaliacoes/views.py

from rest_framework import generics, permissions
from .models import Nota
from .serializers import NotaSerializer

class MeuBoletimView(generics.ListAPIView):
    """
    View para listar todas as notas do usuário logado (o seu boletim).
    """
    serializer_class = NotaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Este método é customizado para garantir que a lista de notas
        retornada seja apenas a do usuário que fez a requisição.
        """
        # self.request.user é o objeto do usuário logado via token.
        return Nota.objects.filter(aluno=self.request.user).select_related('avaliacao__curso')