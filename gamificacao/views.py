from rest_framework import generics, permissions
from .models import ConquistaDoAluno
from .serializers import MinhaConquistaSerializer

from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class MinhasConquistasView(generics.ListAPIView):
    serializer_class = MinhaConquistaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ConquistaDoAluno.objects.filter(aluno=self.request.user).select_related('conquista')
    
class ListaConquistasView(LoginRequiredMixin, View):
    login_url = '/admin/login/'

    def get(self, request):
        conquistas = ConquistaDoAluno.objects.filter(aluno=request.user).select_related('conquista')

        contexto = {
            'lista_de_conquistas': conquistas
        }

        return render(request, 'gamificacao/lista_conquistas.html', contexto)
