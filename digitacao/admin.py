from django.contrib import admin
from .models import LicaoDigitacao, ResultadoDigitacao

@admin.register(LicaoDigitacao)
class LicaoDigitacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'dificuldade')
    list_filter = ('dificuldade',)
    
    search_fields = ('titulo', 'texto')

@admin.register(ResultadoDigitacao)
class ResultadoDigitacaoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'licao', 'palavras_por_minuto', 'precisao', 'data')
    list_filter = ('aluno', 'licao')
    readonly_fields = ('aluno', 'licao', 'palavras_por_minuto', 'precisao', 'data')