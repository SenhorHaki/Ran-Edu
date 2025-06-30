from rest_framework import viewsets, status, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Curso, Modulo, Aula, Inscricao, AulaConcluida, Postagem, Comentario
from .serializers import CursoSerializer, ModuloSerializer, AulaSerializer, InscricaoSerializer, PostagemSerializer, ComentarioSerializer
from .permissions import IsOwnerOrReadOnly
from gamificacao.models import Conquista, ConquistaDoAluno

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def inscrever(self, request, pk=None):
        curso = self.get_object()
        Inscricao.objects.get_or_create(aluno=request.user, curso=curso)
        return Response({'status': 'inscrição realizada'}, status=status.HTTP_201_CREATED)

class ModuloViewSet(viewsets.ModelViewSet):
    queryset = Modulo.objects.all(); serializer_class = ModuloSerializer

class AulaViewSet(viewsets.ModelViewSet):
    queryset = Aula.objects.all(); serializer_class = AulaSerializer
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def marcar_como_concluida(self, request, pk=None):
        aula = self.get_object()
        aluno = request.user

        # 1. Lógica que já tínhamos: verifica se o aluno está inscrito
        curso_da_aula = aula.modulo.curso
        try:
            inscricao = Inscricao.objects.get(aluno=aluno, curso=curso_da_aula)
        except Inscricao.DoesNotExist:
            return Response(
                {'detail': 'Você não está inscrito no curso desta aula.'},
                status=status.HTTP_403_FORBIDDEN
            )

            # 2. Lógica que já tínhamos: Marca a aula como concluída
        AulaConcluida.objects.get_or_create(aluno=aluno, aula=aula)

        # 3. Lógica que já tínhamos: Recalcula o progresso do aluno no curso
        total_aulas_curso = Aula.objects.filter(modulo__curso=curso_da_aula).count()
        aulas_concluidas_pelo_aluno = AulaConcluida.objects.filter(
            aluno=aluno, aula__modulo__curso=curso_da_aula
        ).count()

        progresso = 0
        if total_aulas_curso > 0:
            progresso = round((aulas_concluidas_pelo_aluno / total_aulas_curso) * 100)

        inscricao.progresso = progresso
        inscricao.save()

        # --- INÍCIO DA NOSSA NOVA LÓGICA DE GAMIFICAÇÃO ---

        # 4. Verifica se esta é a primeira aula concluída pelo aluno na plataforma
        total_aulas_concluidas_geral = AulaConcluida.objects.filter(aluno=aluno).count()

        if total_aulas_concluidas_geral == 1:
            try:
                # 5. Busca a conquista "Primeiros Passos" (assumindo que ela tem ID 1)
                conquista_iniciante = Conquista.objects.get(id=1)

                # 6. Concede a conquista ao aluno
                ConquistaDoAluno.objects.get_or_create(aluno=aluno, conquista=conquista_iniciante)

                # Poderíamos até adicionar uma mensagem especial na resposta!
                return Response({
                    'status': 'aula concluída',
                    'progresso_atual_do_curso': f'{progresso}%',
                    'nova_conquista': conquista_iniciante.nome # <-- Mensagem de Bônus!
            }, status=status.HTTP_200_OK)

            except Conquista.DoesNotExist:
            # Se a conquista com ID 1 não for encontrada, não faz nada.
                pass 

            # --- FIM DA NOVA LÓGICA DE GAMIFICAÇÃO ---

            # Se não for a primeira aula, retorna a resposta padrão
        return Response({
        'status': 'aula concluída',
        'progresso_atual_do_curso': f'{progresso}%'
        }, status=status.HTTP_200_OK)


class MinhasInscricoesView(generics.ListAPIView):
    serializer_class = InscricaoSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self): return Inscricao.objects.filter(aluno=self.request.user)


class PostagemViewSet(viewsets.ModelViewSet):
    """
    API endpoint para as postagens do fórum.
    """
    queryset = Postagem.objects.all()
    serializer_class = PostagemSerializer
    # A permissão padrão (IsAuthenticated) que definimos em settings.py já se aplica aqui.

    def perform_create(self, serializer):
        # Associa o autor da postagem ao usuário logado automaticamente.
        serializer.save(autor=self.request.user)


class ComentarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para os comentários do fórum.
    """
    queryset = Comentario.objects.select_related('autor', 'postagem').all()
    serializer_class = ComentarioSerializer
    # APLICA NOSSA NOVA REGRA DE PERMISSÃO AQUI
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Associa o autor do comentário ao usuário logado automaticamente.
        serializer.save(autor=self.request.user)
