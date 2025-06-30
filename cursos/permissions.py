from rest_framework import permissions

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
