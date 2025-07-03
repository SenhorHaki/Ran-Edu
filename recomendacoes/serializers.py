from rest_framework import serializers
from .models import MaterialComplementar

class MaterialComplementarSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialComplementar
        fields = ['id', 'titulo', 'tipo', 'link', 'descricao', 'curso']