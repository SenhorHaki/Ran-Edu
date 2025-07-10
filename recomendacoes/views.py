from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from cursos.models import Inscricao
from .models import MaterialComplementar

class RecomendacaoView(LoginRequiredMixin, View):
    login_url = '/admin/login/'
    template_name = 'recomendacoes/lista_recomendacoes.html'

    def get(self, request):
        cursos_inscritos_ids = Inscricao.objects.filter(
            aluno=request.user
        ).values_list('curso_id', flat=True)

        recomendacoes = MaterialComplementar.objects.filter(curso_id__in=cursos_inscritos_ids)

        contexto = {
            'recomendacoes': recomendacoes
        }

        return render(request, self.template_name, contexto)