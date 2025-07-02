# Em dashboard/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from cursos.models import Inscricao
from gamificacao.models import ConquistaDoAluno
from notificacoes.models import Notificacao
from .serializers import DashboardSerializer

class DashboardView(APIView):
    """
    View que agrega múltiplos dados para o dashboard do usuário logado.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        usuario = request.user

        # 1. Busca cursos em andamento
        cursos = Inscricao.objects.filter(aluno=usuario).select_related('curso')

        # 2. Busca as 5 últimas conquistas
        conquistas = ConquistaDoAluno.objects.filter(aluno=usuario).select_related('conquista').order_by('-data_obtencao')[:5]
        
        # 3. Conta notificações não lidas
        notificacoes_count = Notificacao.objects.filter(destinatario=usuario, lida=False).count()

        # Monta o objeto de dados para o serializer
        dashboard_data = {
            'username': usuario.username,
            'cursos_em_andamento': cursos,
            'ultimas_conquistas': conquistas,
            'notificacoes_nao_lidas': notificacoes_count
        }

        # Serializa os dados agregados
        serializer = DashboardSerializer(instance=dashboard_data)

        return Response(serializer.data)

