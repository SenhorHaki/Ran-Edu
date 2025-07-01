from rest_framework import generics, permissions
from .models import ConquistaDoAluno
from .serializers import MinhaConquistaSerializer

class MinhasConquistasView(generics.ListAPIView):
    """
    View para listar todas as conquistas obtidas pelo usuário logado.
    """
    serializer_class = MinhaConquistaSerializer
    # Garante que apenas usuários autenticados possam acessar esta view.
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Este método é o coração da nossa segurança e personalização.
        Ele garante que a lista de conquistas retornada
        seja apenas a do usuário que fez a requisição.
        """
        # self.request.user é o objeto do usuário atualmente logado (identificado pelo token).
        return ConquistaDoAluno.objects.filter(aluno=self.request.user).select_related('conquista')