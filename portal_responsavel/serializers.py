from rest_framework import serializers
from cursos.models import Inscricao
from avaliacoes.models import Nota
from usuarios.models import Usuario

class ProgressoCursoSerializer(serializers.ModelSerializer):
    """ Mostra o progresso de um aluno em um curso específico. """
    # Acessa o título do curso através da relação com a inscrição
    titulo_curso = serializers.ReadOnlyField(source='curso.titulo')

    class Meta:
        model = Inscricao
        fields = ['titulo_curso', 'progresso']

class BoletimAlunoSerializer(serializers.ModelSerializer):
    """ Mostra a nota de um aluno em uma avaliação específica. """
    # Acessa o título da avaliação
    titulo_avaliacao = serializers.ReadOnlyField(source='avaliacao.titulo')

    class Meta:
        model = Nota
        fields = ['titulo_avaliacao', 'valor']

class AlunoParaResponsavelSerializer(serializers.ModelSerializer):
    """
    O serializer principal que junta todas as informações de um aluno
    para serem exibidas no portal do responsável.
    """
    # Usa os serializers que criamos acima para aninhar os dados
    cursos_em_andamento = ProgressoCursoSerializer(source='inscricao_set', many=True, read_only=True)
    boletim = BoletimAlunoSerializer(source='notas', many=True, read_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id', 
            'username', 
            'first_name', 
            'last_name',
            'cursos_em_andamento', # Lista de cursos e progressos
            'boletim'              # Lista de notas
        ]
