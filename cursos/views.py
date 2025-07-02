from django.db.models import Count
from rest_framework import viewsets, status, generics, permissions
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Certificado, Curso, Modulo, Aula, Inscricao, AulaConcluida, Postagem, Comentario
from .serializers import CursoSerializer, ModuloSerializer, AulaSerializer, InscricaoSerializer, PostagemSerializer, ComentarioSerializer
from .permissions import IsOwnerOrReadOnly, IsEnrolled
from gamificacao.models import Conquista, ConquistaDoAluno
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

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
    queryset = Aula.objects.all()
    serializer_class = AulaSerializer
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def marcar_como_concluida(self, request, pk=None):
        aula = self.get_object()
        aluno = request.user

        # Lógica para verificar inscrição
        curso_da_aula = aula.modulo.curso
        try:
            inscricao = Inscricao.objects.get(aluno=aluno, curso=curso_da_aula)
        except Inscricao.DoesNotExist:
            return Response(
                {'detail': 'Você não está inscrito no curso desta aula.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Lógica para marcar aula como concluída
        AulaConcluida.objects.get_or_create(aluno=aluno, aula=aula)
        
        # Lógica para recalcular progresso
        total_aulas_curso = Aula.objects.filter(modulo__curso=curso_da_aula).count()
        aulas_concluidas_pelo_aluno = AulaConcluida.objects.filter(
            aluno=aluno, aula__modulo__curso=curso_da_aula
        ).count()
        
        progresso = 0
        if total_aulas_curso > 0:
            progresso = round((aulas_concluidas_pelo_aluno / total_aulas_curso) * 100)
        inscricao.progresso = progresso
        inscricao.save()

        # --- LÓGICA DE RECOMPENSAS (Gamificação e Certificado) ---
        
        mensagem_bonus = {} # Dicionário para guardar mensagens especiais

        # Lógica de Gamificação (que você já tinha)
        total_aulas_concluidas_geral = AulaConcluida.objects.filter(aluno=aluno).count()
        if total_aulas_concluidas_geral == 1:
            try:
                conquista_iniciante = Conquista.objects.get(id=1)
                ConquistaDoAluno.objects.get_or_create(aluno=aluno, conquista=conquista_iniciante)
                mensagem_bonus['nova_conquista'] = conquista_iniciante.nome
            except Conquista.DoesNotExist:
                pass 
        
        if inscricao.progresso == 100:
            certificado, created = Certificado.objects.get_or_create(inscricao=inscricao)
            if created:
                mensagem_bonus['aviso_certificado'] = "Parabéns! Seu certificado está disponível para download."

        resposta_final = {
            'status': 'aula concluída',
            'progresso_atual_do_curso': f'{progresso}%'
        }
        resposta_final.update(mensagem_bonus) 

        return Response(resposta_final, status=status.HTTP_200_OK)

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

    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_fields = ['curso']

    search_fields = ['titulo', 'conteudo']

    permission_classes = [permissions.IsAuthenticated, IsEnrolled]

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
        """
        Customiza a criação de um comentário para lidar com respostas.
        """
        parent_comment = serializer.validated_data.get('parent', None)

        if parent_comment:
            serializer.save(autor=self.request.user, postagem=parent_comment.postagem)
        else:
            serializer.save(autor=self.request.user)

class GerarCertificadoView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Pega o ID da inscrição a partir da URL
        inscricao_id = self.kwargs.get('inscricao_id')

        try:
            # Garante que a inscrição existe E pertence ao usuário logado
            inscricao = Inscricao.objects.get(id=inscricao_id, aluno=request.user)
        except Inscricao.DoesNotExist:
            return Response({"detail": "Inscrição não encontrada ou não pertence a você."}, status=status.HTTP_404_NOT_FOUND)

        # Regra de negócio: SÓ gera certificado se o progresso for 100%
        if inscricao.progresso < 100:
            return Response({"detail": "Você precisa concluir 100% do curso para emitir o certificado."}, status=status.HTTP_403_FORBIDDEN)

        # Busca ou cria o registro do certificado para garantir que temos um código de validação
        certificado, created = Certificado.objects.get_or_create(inscricao=inscricao)

        # Prepara os dados para o template HTML
        contexto = {
            'aluno_nome': inscricao.aluno.get_full_name() or inscricao.aluno.username,
            'curso_titulo': inscricao.curso.titulo,
            'carga_horaria': inscricao.curso.carga_horaria,
            'data_emissao': certificado.data_emissao.strftime('%d de %B de %Y'),
            'codigo_validacao': certificado.codigo_validacao
        }

        # Renderiza o template HTML com os dados
        html_string = render_to_string('cursos/certificado_template.html', contexto)

        # Gera o PDF a partir do HTML
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        pdf = html.write_pdf()

        # Cria a resposta HTTP com o PDF para download
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="certificado-{inscricao.curso.titulo}.pdf"'

        return response
