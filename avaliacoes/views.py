from rest_framework import generics, permissions
from .models import Nota
from .serializers import NotaSerializer

from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class MeuBoletimView(generics.ListAPIView):
    serializer_class = NotaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Nota.objects.filter(aluno=self.request.user).select_related('avaliacao__curso')
    
class BoletimView(LoginRequiredMixin, View):
    login_url = '/admin/login/'

    def get(self, request):
        notas = Nota.objects.filter(aluno=request.user).select_related('avaliacao__curso')
        contexto = {
            'notas': notas
        }
        
        return render(request, 'avaliacoes/boletim.html', contexto)
    