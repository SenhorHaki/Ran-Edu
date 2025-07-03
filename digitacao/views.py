from rest_framework import viewsets, mixins, permissions
from .models import LicaoDigitacao, ResultadoDigitacao
from .serializers import LicaoDigitacaoSerializer, ResultadoDigitacaoSerializer

class LicaoDigitacaoViewSet(viewsets.ReadOnlyModelViewSet):
    """ ViewSet para listar e ver detalhes das lições de digitação. (Apenas leitura) """
    queryset = LicaoDigitacao.objects.all()
    serializer_class = LicaoDigitacaoSerializer
    permission_classes = [permissions.IsAuthenticated]

class ResultadoDigitacaoViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ ViewSet para que um aluno possa salvar seu resultado. (Apenas criação) """
    queryset = ResultadoDigitacao.objects.all()
    serializer_class = ResultadoDigitacaoSerializer
    permission_classes = [permissions.IsAuthenticated]