# Em portal_responsavel/views.py

from rest_framework import generics, permissions
from usuarios.models import Usuario, ResponsavelAluno
from .serializers import AlunoParaResponsavelSerializer

class PortalResponsavelView(generics.ListAPIView):
    """
    View principal do Portal do Responsável.
    Lista todos os alunos associados ao responsável logado.
    """
    serializer_class = AlunoParaResponsavelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # O usuário logado (o responsável) é pego da requisição
        responsavel = self.request.user

        # Busca na tabela de relação os IDs de todos os alunos deste responsável
        aluno_ids = ResponsavelAluno.objects.filter(
            responsavel=responsavel
        ).values_list('aluno_id', flat=True)

        # Retorna os objetos de Usuario para cada um desses IDs de aluno
        return Usuario.objects.filter(id__in=aluno_ids).prefetch_related(
            'inscricao_set__curso',
            'notas__avaliacao'
        )