from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, ResponsavelAluno

class CustomUserAdmin(UserAdmin):
    # Adiciona o campo 'tipo' ao formulário de edição do usuário no admin
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('tipo',)}),
    )
    # Adiciona a coluna 'tipo' na lista de usuários
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'tipo')

admin.site.register(ResponsavelAluno)

admin.site.register(Usuario, CustomUserAdmin)
