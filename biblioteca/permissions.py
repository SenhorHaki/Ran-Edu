from rest_framework import permissions
from usuarios.models import Usuario

class IsProfessor(permissions.BasePermission):
    """
    Permissão que só permite o acesso a usuários do tipo Professor.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo == Usuario.TipoUsuario.PROFESSOR