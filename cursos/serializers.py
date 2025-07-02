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

class RespostaSerializer(serializers.ModelSerializer):
    """
    Este é um Serializer SIMPLES, apenas para as respostas.
    Ele não tenta aninhar mais respostas dentro dele, evitando o loop.
    """
    autor_username = serializers.ReadOnlyField(source='autor.username')

    class Meta:
        model = Comentario
        fields = ['id', 'postagem', 'parent', 'autor', 'autor_username', 'conteudo', 'data_criacao', 'data_edicao']

class ComentarioSerializer(serializers.ModelSerializer):
    autor_username = serializers.ReadOnlyField(source='autor.username')
    respostas = RespostaSerializer(many=True, read_only=True)

    class Meta:
        model = Comentario
        fields = ['id', 'postagem', 'parent', 'autor', 'autor_username', 'conteudo', 'data_criacao', 'data_edicao', 'respostas']
        extra_kwargs = {
            'autor': {'read_only': True},
            # Dizemos que postagem e parent não são obrigatórios no input
            'postagem': {'required': False, 'allow_null': True},
            'parent': {'required': False, 'allow_null': True},
    }
        
class PostagemSerializer(serializers.ModelSerializer):
    autor = serializers.HiddenField(default=serializers.CurrentUserDefault())
    autor_username = serializers.ReadOnlyField(source='autor.username')
    comentarios = ComentarioSerializer(many=True, read_only=True)

    num_comentarios = serializers.IntegerField(read_only=True)

    class Meta:
        model = Postagem
        fields = ['id', 'curso', 'titulo', 'autor', 'autor_username', 'conteudo', 'data_criacao', 'comentarios', 'num_comentarios']