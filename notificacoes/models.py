from django.db import models
from django.conf import settings

class Notificacao(models.Model):
    destinatario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notificacoes'
    )
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_criacao'] # Mostra as mais recentes primeiro

    def __str__(self):
        return f"Notificação para {self.destinatario.username}: {self.mensagem[:30]}..."
