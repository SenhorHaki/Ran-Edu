from rest_framework import generics, permissions
from cursos.models import Inscricao
from .models import Evento
from .serializers import EventoSerializer

class AgendaView(generics.ListAPIView):
    serializer_class = EventoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cursos_inscritos_ids = Inscricao.objects.filter(
            aluno=self.request.user
        ).values_list('curso_id', flat=True)

        return Evento.objects.filter(curso_id__in=cursos_inscritos_ids)