from django.contrib import admin
from .models import Avaliacao, Nota

# Registra os modelos para que eles apareçam na interface de administração.
admin.site.register(Avaliacao)
admin.site.register(Nota)