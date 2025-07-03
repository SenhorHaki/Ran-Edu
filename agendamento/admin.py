from django.contrib import admin
from .models import Evento

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'curso', 'tipo', 'data_inicio', 'data_fim')
    list_filter = ('tipo', 'curso')
    search_fields = ('titulo', 'descricao', 'curso__titulo')