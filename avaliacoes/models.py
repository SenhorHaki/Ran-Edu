from django.db import models
from django.conf import settings
from cursos.models import Curso # Precisamos saber a qual curso a avaliação pertence

class Avaliacao(models.Model):
    """
    Representa uma atividade avaliativa, como uma prova ou um trabalho.
    """
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='avaliacoes')
    titulo = models.CharField(max_length=200, help_text="Ex: Prova 1, Trabalho Final")
    # Campos como 'data_limite' ou 'peso' poderiam ser adicionados aqui no futuro.

    def __str__(self):
        return f"{self.titulo} - {self.curso.titulo}"

class Nota(models.Model):
    """
    Registra a nota de um aluno específico em uma avaliação específica.
    """
    aluno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notas')
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, related_name='notas')
    # Usamos DecimalField para notas, pois é mais preciso para números decimais como 7,5
    valor = models.DecimalField(max_digits=5, decimal_places=2, help_text="Nota do aluno, ex: 8.50, 10.00")
    data_lancamento = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Garante que um aluno tenha apenas uma nota por avaliação.
        unique_together = [['aluno', 'avaliacao']]

    def __str__(self):
        return f'Nota de {self.aluno.username} em {self.avaliacao.titulo}: {self.valor}'