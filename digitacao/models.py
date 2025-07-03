# Em digitacao/models.py
from django.db import models
from django.conf import settings

class LicaoDigitacao(models.Model):
    """
    Armazena uma lição de digitação, com o texto a ser digitado.
    """
    titulo = models.CharField(max_length=100, help_text="Ex: 'Frases Curtas', 'Parágrafo Técnico'")
    texto = models.TextField()
    # No futuro, podemos adicionar um campo de dificuldade (Fácil, Médio, Difícil)

    def __str__(self):
        return self.titulo

class ResultadoDigitacao(models.Model):
    """
    Armazena o resultado de uma tentativa de um aluno em uma lição.
    """
    aluno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resultados_digitacao')
    licao = models.ForeignKey(LicaoDigitacao, on_delete=models.CASCADE)
    palavras_por_minuto = models.PositiveIntegerField()
    precisao = models.FloatField(help_text="Ex: 98.5 para 98.5% de precisão")
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data']

    def __str__(self):
        return f"Resultado de {self.aluno.username} em {self.licao.titulo}"