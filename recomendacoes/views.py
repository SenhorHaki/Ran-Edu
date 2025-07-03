from rest_framework import generics, permissions
from cursos.models import Inscricao
from .models import MaterialComplementar
from .serializers import MaterialComplementarSerializer

class RecomendacaoListView(generics.ListAPIView):
    serializer_class = MaterialComplementarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 1. Encontra os IDs de todos os cursos em que o aluno está inscrito.
        cursos_inscritos_ids = Inscricao.objects.filter(
            aluno=self.request.user
        ).values_list('curso_id', flat=True)

        # 2. Retorna todos os materiais complementares que pertencem a esses cursos.
        return MaterialComplementar.objects.filter(curso_id__in=cursos_inscritos_ids)
