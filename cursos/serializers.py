from rest_framework import serializers
from .models import Curso, Modulo, Aula, Inscricao, Postagem, Comentario, Turma

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
    num_modulos = serializers.IntegerField(read_only=True)
    num_aulas = serializers.IntegerField(read_only=True)
    class Meta: 
        model = Curso
        fields = ['id', 'titulo', 'descricao', 'carga_horaria', 'num_modulos', 'num_aulas', 'modulos', 'inscricoes']

class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = '__all__'

class RespostaSerializer(serializers.ModelSerializer):
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
        fields = ['id', 'curso', 'turma', 'titulo', 'autor', 'autor_username', 'conteudo', 'data_criacao', 'comentarios', 'num_comentarios']
        extra_kwargs = {
            'curso': {'required': False, 'allow_null': True},
            'turma': {'required': False, 'allow_null': True},
        }