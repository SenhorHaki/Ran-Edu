from .serializers import LicaoDigitacaoSerializer, ResultadoDigitacaoSerializer

from .models import LicaoDigitacao, ResultadoDigitacao


from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import viewsets, mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
import json


class LicaoDigitacaoViewSet(viewsets.ReadOnlyModelViewSet):
    """ ViewSet para listar e ver detalhes das lições de digitação. """
    queryset = LicaoDigitacao.objects.all()
    serializer_class = LicaoDigitacaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def leaderboard(self, request, pk=None):
        """
        Retorna o placar de líderes (top 10) para esta lição específica.
        URL: /api/digitacao/licoes/{id_da_licao}/leaderboard/
        """
        licao = self.get_object() # Pega a lição pelo ID da URL
        
        # Busca os 10 melhores resultados para esta lição, ordenados
        top_resultados = ResultadoDigitacao.objects.filter(licao=licao).order_by(
            '-palavras_por_minuto', # Maior velocidade primeiro
            '-precisao'             # Em caso de empate, maior precisão
        )[:10]
        
        # Usa o serializer de resultados para formatar a resposta
        serializer = ResultadoDigitacaoSerializer(top_resultados, many=True)
        return Response(serializer.data)

class ResultadoDigitacaoViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ResultadoDigitacao.objects.all()
    serializer_class = ResultadoDigitacaoSerializer
    permission_classes = [permissions.IsAuthenticated]   
    authentication_classes = [SessionAuthentication, JWTAuthentication]


class GameView(LoginRequiredMixin, View):
    login_url = '/admin/login/'
    template_name = 'digitacao/game.html'

    def get(self, request):
        licoes = LicaoDigitacao.objects.all()
        licoes_json = serialize('json', licoes, fields=('pk', 'titulo', 'texto', 'dificuldade'))

        contexto = {
            'licoes_json': licoes_json
        }

        return render(request, self.template_name, contexto)
