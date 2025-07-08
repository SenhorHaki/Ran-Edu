# Em cursos/admin.py

from django.contrib import admin
from .models import (
    Curso,
    Turma,
    Modulo,
    Aula,
    Inscricao,
    Postagem,
    Comentario,
    AulaConcluida,
    Certificado 
)

admin.site.register(Curso)
admin.site.register(Modulo)
admin.site.register(Aula)
admin.site.register(Postagem)
admin.site.register(Comentario)
admin.site.register(AulaConcluida)
admin.site.register(Certificado)

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'curso')
    list_filter = ('curso',)
    search_fields = ('nome', 'curso__titulo')
    filter_horizontal = ('alunos',)

@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    list_display = ('id','aluno', 'curso', 'progresso', 'data_inscricao')
    list_filter = ('curso',)
    search_fields = ('aluno__username', 'curso__titulo')
    