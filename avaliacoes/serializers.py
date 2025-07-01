# Em avaliacoes/serializers.py

from rest_framework import serializers
from .models import Avaliacao, Nota

class AvaliacoSerializer(serializers.ModelSerializer):
    """
    Serializer simples para os detalhes de uma Avaliação (ex: Prova 1).
    """
    class Meta:
        model = Avaliacao
        fields = ['id', 'titulo', 'curso']


class NotaSerializer(serializers.ModelSerializer):
    """
    Serializer para a Nota de um aluno.
    Ele mostra os detalhes da avaliação aninhados para dar mais contexto.
    """
    # Aninha o AvaliacaoSerializer para mostrar os detalhes da prova/trabalho,
    # não apenas o ID dela.
    avaliacao = AvaliacoSerializer(read_only=True)
    
    # Adiciona o nome do aluno na resposta para mais clareza.
    aluno_username = serializers.ReadOnlyField(source='aluno.username')

    class Meta:
        model = Nota
        fields = ['id', 'aluno_username', 'avaliacao', 'valor', 'data_lancamento']