# Em portal_responsavel/views.py
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from usuarios.models import Usuario, ResponsavelAluno

class PortalView(LoginRequiredMixin, View):
    login_url = '/admin/login/'
    template_name = 'portal_responsavel/portal.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.tipo != Usuario.TipoUsuario.RESPONSAVEL:
            return redirect('dashboard:home') # Redireciona para o dashboard se não for responsável
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        responsavel = request.user
        aluno_ids = ResponsavelAluno.objects.filter(
            responsavel=responsavel
        ).values_list('aluno_id', flat=True)

        alunos_associados = Usuario.objects.filter(id__in=aluno_ids).prefetch_related(
            'inscricao_set__curso',
            'notas__avaliacao'
        )

        contexto = {
            'alunos_associados': alunos_associados
        }

        return render(request, self.template_name, contexto)