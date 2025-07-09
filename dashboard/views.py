from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from cursos.models import Inscricao

from gamificacao.models import ConquistaDoAluno

from notificacoes.models import Notificacao

from .serializers import DashboardSerializer

class DashboardView(LoginRequiredMixin, View):
    login_url = '/admin/login/' 

    def get(self, request, *args, **kwargs):
        usuario = request.user

        cursos = Inscricao.objects.filter(aluno=usuario).select_related('curso')
        conquistas = ConquistaDoAluno.objects.filter(aluno=usuario).select_related('conquista').order_by('-data_obtencao')[:5]
        notificacoes_count = Notificacao.objects.filter(destinatario=usuario, lida=False).count()

        contexto = {
            'cursos_em_andamento': cursos,
            'ultimas_conquistas': conquistas,
            'notificacoes_nao_lidas': notificacoes_count,
        }

        return render(request, 'dashboard/home.html', contexto)
