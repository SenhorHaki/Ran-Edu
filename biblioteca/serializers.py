# Em biblioteca/serializers.py
from rest_framework import serializers
from .models import Recurso

class RecursoSerializer(serializers.ModelSerializer):
    autor = serializers.HiddenField(default=serializers.CurrentUserDefault())
    autor_username = serializers.ReadOnlyField(source='autor.username')

    # A class Meta precisa estar indentada aqui dentro
    class Meta:
        model = Recurso
        fields = ['id', 'titulo', 'descricao', 'arquivo', 'autor', 'autor_username', 'data_upload', 'curso']