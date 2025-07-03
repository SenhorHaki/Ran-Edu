from django.contrib import admin
from .models import MaterialComplementar

@admin.register(MaterialComplementar)
class MaterialComplementarAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'curso', 'tipo')
    list_filter = ('tipo', 'curso')
    search_fields = ('titulo', 'descricao', 'curso__titulo')

