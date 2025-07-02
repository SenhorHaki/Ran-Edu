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

@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    # Define as colunas que aparecerão na tabela
    list_display = ('id','aluno', 'curso', 'progresso', 'data_inscricao')

    # Cria uma barra lateral de filtros (neste caso, para filtrar por curso)
    list_filter = ('curso',)

    # Adiciona uma barra de busca no topo
    search_fields = ('aluno__username', 'curso__titulo')


admin.site.register(Postagem)
admin.site.register(Comentario)
admin.site.register(AulaConcluida)