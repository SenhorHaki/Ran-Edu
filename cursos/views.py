from django.db.models import Count
from rest_framework import viewsets, status, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Curso, Modulo, Aula, Inscricao, AulaConcluida, Postagem, Comentario
from .serializers import CursoSerializer, ModuloSerializer, AulaSerializer, InscricaoSerializer, PostagemSerializer, ComentarioSerializer
from .permissions import IsOwnerOrReadOnly
from gamificacao.models import Conquista, ConquistaDoAluno

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.annotate(
        num_modulos=Count('modulos', distinct=True),
        num_aulas=Count('modulos__aulas', distinct=True)
    ).prefetch_related('modulos__aulas')

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

        curso_da_aula = aula.modulo.curso
        try:
            inscricao = Inscricao.objects.get(aluno=aluno, curso=curso_da_aula)
        except Inscricao.DoesNotExist:
            return Response(
                {'detail': 'Você não está inscrito no curso desta aula.'},
                status=status.HTTP_403_FORBIDDEN
            )

        AulaConcluida.objects.get_or_create(aluno=aluno, aula=aula)

        total_aulas_curso = Aula.objects.filter(modulo__curso=curso_da_aula).count()
        aulas_concluidas_pelo_aluno = AulaConcluida.objects.filter(
            aluno=aluno, aula__modulo__curso=curso_da_aula
        ).count()

        progresso = 0
        if total_aulas_curso > 0:
            progresso = round((aulas_concluidas_pelo_aluno / total_aulas_curso) * 100)

        inscricao.progresso = progresso
        inscricao.save()

        total_aulas_concluidas_geral = AulaConcluida.objects.filter(aluno=aluno).count()

        if total_aulas_concluidas_geral == 1:
            try:
                conquista_iniciante = Conquista.objects.get(id=1)

                ConquistaDoAluno.objects.get_or_create(aluno=aluno, conquista=conquista_iniciante)

                return Response({
                    'status': 'aula concluída',
                    'progresso_atual_do_curso': f'{progresso}%',
                    'nova_conquista': conquista_iniciante.nome # <-- Mensagem de Bônus!
            }, status=status.HTTP_200_OK)

            except Conquista.DoesNotExist:
                pass 

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
    queryset = Postagem.objects.select_related('autor', 'curso').annotate(
        num_comentarios=Count('comentarios', distinct=True)
    ).prefetch_related('comentarios__autor')
    
    serializer_class = PostagemSerializer

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)

class ComentarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para os comentários do fórum.
    """
    queryset = Comentario.objects.select_related('autor', 'postagem').all()
    serializer_class = ComentarioSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)
