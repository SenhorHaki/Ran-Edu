from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import generics, permissions

from cursos.models import Inscricao
from .models import MaterialComplementar
from .serializers import MaterialComplementarSerializer

class RecomendacaoListViewAPI(generics.ListAPIView):
    serializer_class = MaterialComplementarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cursos_inscritos_ids = Inscricao.objects.filter(
            aluno=self.request.user
        ).values_list('curso_id', flat=True)

        return MaterialComplementar.objects.filter(curso_id__in=cursos_inscritos_ids)

class RecomendacaoView(LoginRequiredMixin, View):
    login_url = '/admin/login/'
    template_name = 'recomendacoes/lista_recomendacoes.html'

    def get(self, request):
        api_view = RecomendacaoListViewAPI()
        api_view.request = request
        recomendacoes = api_view.get_queryset()
        
        contexto = {
            'recomendacoes': recomendacoes
        }
        
        return render(request, self.template_name, contexto)