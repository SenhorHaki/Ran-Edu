from rest_framework import serializers
from .models import Curso, Modulo, Aula, Inscricao, Postagem, Comentario

class AulaSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Aula
        fields = '__all__'

class ModuloSerializer(serializers.ModelSerializer):
    aulas = AulaSerializer(many=True, read_only=True)
    class Meta: 
        model = Modulo
        fields = '__all__'

class InscricaoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Inscricao
        fields = '__all__'

class CursoSerializer(serializers.ModelSerializer):
    modulos = ModuloSerializer(many=True, read_only=True)
    inscricoes = InscricaoSerializer(many=True, read_only=True, source='inscricao_set')
    class Meta: 
        model = Curso
        fields = '__all__'

class ComentarioSerializer(serializers.ModelSerializer):
    autor_username = serializers.ReadOnlyField(source='autor.username')

    class Meta:
        model = Comentario
        fields = ['id', 'postagem', 'autor', 'autor_username', 'conteudo', 'data_criacao', 'data_edicao']
        extra_kwargs = {'autor': {'read_only': True}}

class PostagemSerializer(serializers.ModelSerializer):
    autor = serializers.HiddenField(default=serializers.CurrentUserDefault())
    autor_username = serializers.ReadOnlyField(source='autor.username')
    comentarios = ComentarioSerializer(many=True, read_only=True)
    num_comentarios = serializers.IntegerField(read_only=True)

    class Meta:
        model = Postagem
        # A lista de fields continua a mesma, pois ela já incluía o campo
        fields = ['id', 'curso', 'titulo', 'autor', 'autor_username', 'conteudo', 'data_criacao', 'comentarios', 'num_comentarios']
