from rest_framework import viewsets, status, generics, permissions
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.db.models import Count, Q
from django.shortcuts import render
from django.views import View

from .models import Certificado, Curso, Modulo, Aula, Inscricao, AulaConcluida, Postagem, Comentario, Turma 
from .serializers import CursoSerializer, ModuloSerializer, AulaSerializer, InscricaoSerializer, PostagemSerializer, ComentarioSerializer
from .permissions import IsOwnerOrReadOnly, IsEnrolled, CanPostInForum
from gamificacao.models import Conquista, ConquistaDoAluno

from weasyprint import HTML
import locale


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
    serializer_class = PostagemSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def get_queryset(self):
        queryset = Postagem.objects.select_related('autor', 'curso', 'turma').annotate(
            num_comentarios=Count('comentarios', distinct=True)
        )
        curso_id = self.request.query_params.get('curso')
        turma_id = self.request.query_params.get('turma')
        escola = self.request.query_params.get('escola')

        if escola:
            return queryset.filter(curso__isnull=True, turma__isnull=True)
        
        if turma_id:
            return queryset.filter(turma_id=turma_id)
        
        if curso_id:
            return queryset.filter(curso_id=curso_id)

        return queryset.none()

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
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):

        try:
            locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
        except locale.Error:
            locale.setlocale(locale.LC_TIME, '')
        
        inscricao_id = self.kwargs.get('inscricao_id')

        try:
            inscricao = Inscricao.objects.get(id=inscricao_id, aluno=request.user)
        except Inscricao.DoesNotExist:
            return Response({"detail": "Inscrição não encontrada ou não pertence a você."}, status=status.HTTP_404_NOT_FOUND)

        if inscricao.progresso < 100:
            return Response({"detail": "Você precisa concluir 100% do curso para emitir o certificado."}, status=status.HTTP_403_FORBIDDEN)

        certificado, created = Certificado.objects.get_or_create(inscricao=inscricao)

        contexto = {
            'aluno_nome': inscricao.aluno.get_full_name() or inscricao.aluno.username,
            'curso_titulo': inscricao.curso.titulo,
            'carga_horaria': inscricao.curso.carga_horaria,
            'data_emissao': certificado.data_emissao.strftime('%d de %B de %Y'),
            'codigo_validacao': certificado.codigo_validacao
        }

        html_string = render_to_string('cursos/certificado_template.html', contexto)

        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        pdf = html.write_pdf()

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="certificado-{inscricao.curso.titulo}.pdf"'

        return response

class ForunsDisponiveisView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        foruns = []

        foruns.append({
            'tipo': 'ESCOLA',
            'nome': 'Fórum da Escola',
            'id': 'escola'
        })

        cursos_inscritos = Inscricao.objects.filter(aluno=user).select_related('curso')
        for inscricao in cursos_inscritos:
            foruns.append({
                'tipo': 'CURSO',
                'nome': f'Fórum - {inscricao.curso.titulo}',
                'id': inscricao.curso.id
            })
            
        turmas_membro = user.turmas_inscritas.all().select_related('curso')
        for turma in turmas_membro:
            foruns.append({
                'tipo': 'TURMA',
                'nome': f'Fórum - {turma.nome}',
                'id': turma.id
            })

        return Response(foruns, status=status.HTTP_200_OK)

class SelecaoForumView(View):
    def get(self, request):
        user = request.user
        foruns = []

        foruns.append({
            'tipo': 'ESCOLA',
            'nome': 'Fórum da Escola',
            'parametro_url': 'escola=true' 
        })

        cursos_inscritos = Inscricao.objects.filter(aluno=user).select_related('curso')
        for inscricao in cursos_inscritos:
            foruns.append({
                'tipo': 'CURSO',
                'nome': f'Fórum - {inscricao.curso.titulo}',
                'parametro_url': f'curso={inscricao.curso.id}'
            })
            
        turmas_membro = user.turmas_inscritas.all().select_related('curso')
        for turma in turmas_membro:
            foruns.append({
                'tipo': 'TURMA',
                'nome': f'Fórum - {turma.nome}',
                'parametro_url': f'turma={turma.id}'
            })

        contexto = {
            'lista_de_foruns': foruns
        }
        
        return render(request, 'cursos/selecao_forum.html', contexto)

class ListaPostagensView(View):
    def get(self, request):
        curso_id = request.GET.get('curso')
        turma_id = request.GET.get('turma')
        escola = request.GET.get('escola')

        queryset = Postagem.objects.select_related('autor', 'curso', 'turma').annotate(
            num_comentarios=Count('comentarios', distinct=True)
        )

        if escola:
            postagens = queryset.filter(curso__isnull=True, turma__isnull=True)
            titulo_forum = "Fórum da Escola"
        elif turma_id:
            postagens = queryset.filter(turma_id=turma_id)
            titulo_forum = f"Fórum da Turma {Turma.objects.get(id=turma_id).nome}"
        elif curso_id:
            postagens = queryset.filter(curso_id=curso_id)
            titulo_forum = f"Fórum do Curso {Curso.objects.get(id=curso_id).titulo}"
        else:
            postagens = queryset.none()
            titulo_forum = "Fórum Inválido"

        contexto = {
            'postagens': postagens,
            'titulo_forum': titulo_forum
        }
        
        return render(request, 'cursos/lista_postagens.html', contexto)

class ListaCertificadosView(LoginRequiredMixin, View):
    login_url = '/admin/login/'

    def get(self, request):
        certificados = Certificado.objects.filter(
            inscricao__aluno=request.user
        ).select_related('inscricao__curso')

        contexto = {
            'lista_de_certificados': certificados
        }

        return render(request, 'cursos/lista_certificados.html', contexto)


