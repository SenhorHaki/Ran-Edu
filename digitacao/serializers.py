from rest_framework import serializers
from .models import LicaoDigitacao, ResultadoDigitacao

class LicaoDigitacaoSerializer(serializers.ModelSerializer):
    dificuldade_display = serializers.CharField(source='get_dificuldade_display', read_only=True)

    class Meta:
        model = LicaoDigitacao
        fields = ['id', 'titulo', 'texto', 'dificuldade', 'dificuldade_display']

class ResultadoDigitacaoSerializer(serializers.ModelSerializer):
    aluno = serializers.HiddenField(default=serializers.CurrentUserDefault())
    aluno_username = serializers.ReadOnlyField(source='aluno.username')

    class Meta:
        model = ResultadoDigitacao
        fields = ['id', 'aluno', 'aluno_username', 'licao', 'palavras_por_minuto', 'precisao', 'data']
        read_only_fields = ['data']
