from django.contrib import admin
from .models import Conquista, ConquistaDoAluno

# Registra os modelos para que eles apareçam na interface de administração.
admin.site.register(Conquista)
admin.site.register(ConquistaDoAluno)