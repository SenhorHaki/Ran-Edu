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
