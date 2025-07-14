from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from cursos.models import Inscricao
from .models import Evento
from rest_framework import generics, permissions
from .serializers import EventoSerializer

class AgendaViewAPI(generics.ListAPIView):
    serializer_class = EventoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cursos_inscritos_ids = Inscricao.objects.filter(aluno=self.request.user).values_list('curso_id', flat=True)
        return Evento.objects.filter(curso_id__in=cursos_inscritos_ids)

class AgendaView(LoginRequiredMixin, View):
    login_url = '/admin/login/'
    template_name = 'agendamento/agenda.html'

    def get(self, request, *args, **kwargs):
        cursos_inscritos_ids = Inscricao.objects.filter(
            aluno=request.user
        ).values_list('curso_id', flat=True)

        eventos = Evento.objects.filter(curso_id__in=cursos_inscritos_ids)
        
        contexto = {
            'eventos': eventos
        }
        
        return render(request, self.template_name, contexto)
