
from django.contrib import admin
from .models import Notificacao

@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    # Define as colunas que aparecerão na lista de notificações
    list_display = ('destinatario', 'mensagem', 'lida', 'data_criacao')
    
    # Cria um filtro na lateral para ver notificações lidas/não lidas
    list_filter = ('lida', 'destinatario')
    
    # Adiciona uma barra de busca
    search_fields = ('destinatario__username', 'mensagem')