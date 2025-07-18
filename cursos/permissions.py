from rest_framework import permissions
from .models import Inscricao

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permissão customizada para permitir que apenas os donos de um objeto
    possam editá-lo ou apagá-lo.
    Outros usuários podem apenas visualizar.
    """
    def has_object_permission(self, request, view, obj):
        # Permissões de leitura (GET, HEAD, OPTIONS) são permitidas para qualquer requisição.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Permissões de escrita (DELETE, PUT, PATCH) só são permitidas
        # se o usuário da requisição for o mesmo que o autor do objeto.
        return obj.autor == request.user

# Em cursos/permissions.py

class CanPostInForum(permissions.BasePermission):
    """
    Permissão para verificar se um usuário pode postar em um determinado fórum.
    """
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True

        if view.action == 'create':
            user = request.user
            data = request.data
            curso_id = data.get('curso')
            turma_id = data.get('turma')

            if turma_id:
                return user.turmas_inscritas.filter(id=turma_id).exists()
            
            if curso_id:
                return Inscricao.objects.filter(aluno=user, curso_id=curso_id).exists()
            
            return True
        
        return True

class IsEnrolled(permissions.BasePermission):
    """
    Permissão que verifica se o usuário está inscrito no curso
    para poder criar uma postagem.
    """
    def has_permission(self, request, view):
        # Permite requisições de leitura (GET) para todos.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Para criar uma postagem (POST), verifica a inscrição.
        curso_id = request.data.get('curso')
        if not curso_id:
            return False # Se não enviou o curso, não tem permissão.
            
        return Inscricao.objects.filter(
            aluno=request.user, 
            curso_id=curso_id
        ).exists()
