from django.db import models
from django.conf import settings

class LicaoDigitacao(models.Model):
    class Dificuldade(models.TextChoices):
        FACIL = 'FACIL', 'Fácil'
        MEDIO = 'MEDIO', 'Médio'
        DIFICIL = 'DIFICIL', 'Difícil'

    titulo = models.CharField(max_length=100, help_text="Ex: 'Frases Curtas', 'Parágrafo Técnico'")
    texto = models.TextField()
    dificuldade = models.CharField(
        max_length=10,
        choices=Dificuldade.choices,
        default=Dificuldade.FACIL
    )

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
    