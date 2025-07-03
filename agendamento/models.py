from django.db import models
from cursos.models import Curso

class Evento(models.Model):
    TIPO_EVENTO_CHOICES = [
        ('AULA_AO_VIVO', 'Aula ao Vivo'),
        ('PROVA', 'Prova'),
        ('ENTREGA_TRABALHO', 'Entrega de Trabalho'),
        ('OUTRO', 'Outro'),
    ]

    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='eventos')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    tipo = models.CharField(max_length=20, choices=TIPO_EVENTO_CHOICES, default='AULA_AO_VIVO')

    class Meta:
        ordering = ['data_inicio']

    def __str__(self):
        return f"{self.get_tipo_display()}: {self.titulo} - {self.curso.titulo}"