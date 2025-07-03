from rest_framework import serializers
from .models import LicaoDigitacao, ResultadoDigitacao

class LicaoDigitacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicaoDigitacao
        fields = ['id', 'titulo', 'texto']

class ResultadoDigitacaoSerializer(serializers.ModelSerializer):
    aluno = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ResultadoDigitacao
        fields = ['id', 'aluno', 'licao', 'palavras_por_minuto', 'precisao', 'data']
        read_only_fields = ['data']
