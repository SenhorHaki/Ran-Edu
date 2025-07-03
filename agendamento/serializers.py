from rest_framework import serializers
from .models import Evento

class EventoSerializer(serializers.ModelSerializer):
    # Para facilitar para o frontend, incluímos o nome do tipo do evento
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)

    class Meta:
        model = Evento
        fields = ['id', 'titulo', 'descricao', 'data_inicio', 'data_fim', 'tipo', 'tipo_display', 'curso']