from django.contrib import admin
from .models import Recurso

@admin.register(Recurso)
class RecursoAdmin(admin.ModelAdmin):
    # Campos que serão exibidos na lista de recursos
    list_display = ('titulo', 'autor', 'data_upload')
    
    # Filtro por autor
    list_filter = ('autor',)
    
    # Campos de busca
    search_fields = ('titulo', 'descricao', 'autor__username')