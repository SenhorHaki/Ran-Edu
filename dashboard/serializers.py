# Em dashboard/serializers.py

from rest_framework import serializers
from cursos.models import Inscricao
from gamificacao.models import ConquistaDoAluno

class ResumoCursoSerializer(serializers.ModelSerializer):
    """ Serializer para um resumo rápido dos cursos do aluno. """
    titulo_curso = serializers.CharField(source='curso.titulo')
    
    class Meta:
        model = Inscricao
        fields = ['titulo_curso', 'progresso']


class ResumoConquistaSerializer(serializers.ModelSerializer):
    """ Serializer para um resumo rápido das últimas conquistas. """
    nome_conquista = serializers.CharField(source='conquista.nome')
    icone_conquista = serializers.CharField(source='conquista.icone')

    class Meta:
        model = ConquistaDoAluno
        fields = ['nome_conquista', 'icone_conquista', 'data_obtencao']


class DashboardSerializer(serializers.Serializer):
    """
    Este serializer não é de um modelo, ele junta dados de várias fontes.
    """
    username = serializers.CharField()
    cursos_em_andamento = ResumoCursoSerializer(many=True)
    ultimas_conquistas = ResumoConquistaSerializer(many=True)
    notificacoes_nao_lidas = serializers.IntegerField()