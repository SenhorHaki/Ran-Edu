from django.contrib import admin
from .models import (
    Curso,
    Modulo,
    Aula,
    Inscricao,
    Postagem,
    Comentario,
    AulaConcluida
)

# Registra todos os modelos para que eles apareçam na interface de administração
admin.site.register(Curso)
admin.site.register(Modulo)
admin.site.register(Aula)
admin.site.register(Inscricao)
admin.site.register(Postagem)
admin.site.register(Comentario)
admin.site.register(AulaConcluida)