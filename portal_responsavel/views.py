from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import generics, permissions

from usuarios.models import Usuario, ResponsavelAluno
from .serializers import AlunoParaResponsavelSerializer

class PortalResponsavelView(generics.ListAPIView):
    serializer_class = AlunoParaResponsavelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        responsavel = self.request.user
        aluno_ids = ResponsavelAluno.objects.filter(
            responsavel=responsavel
        ).values_list('aluno_id', flat=True)
        return Usuario.objects.filter(id__in=aluno_ids).prefetch_related(
            'inscricao_set__curso', 
            'notas__avaliacao'
        )

class PortalView(LoginRequiredMixin, View):
    login_url = '/admin/login/'
    template_name = 'portal_responsavel/portal.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.tipo != Usuario.TipoUsuario.RESPONSAVEL:
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        api_view = PortalResponsavelView()
        api_view.request = request
        alunos_associados = api_view.get_queryset()
        
        contexto = {
            'alunos_associados': alunos_associados
        }
        
        return render(request, self.template_name, contexto)