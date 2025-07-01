from rest_framework import serializers
from .models import Conquista, ConquistaDoAluno

class ConquistaSerializer(serializers.ModelSerializer):
    """
    Serializer para os detalhes de uma Conquista (a medalha em si).
    """
    class Meta:
        model = Conquista
        fields = ['nome', 'descricao', 'icone']


class MinhaConquistaSerializer(serializers.ModelSerializer):
    """
    Serializer para listar as conquistas de um aluno.
    Ele "aninha" o ConquistaSerializer para mostrar os detalhes da medalha.
    """
    # Usamos o nome do campo no modelo 'ConquistaDoAluno' (conquista)
    # e o serializer que queremos usar para ele.
    conquista = ConquistaSerializer(read_only=True)

    class Meta:
        model = ConquistaDoAluno
        fields = ['conquista', 'data_obtencao']