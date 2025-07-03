from django.db import models
from cursos.models import Curso

class MaterialComplementar(models.Model):
    TIPO_CHOICES = [
        ('VIDEO', 'Vídeo'),
        ('ARTIGO', 'Artigo'),
        ('LIVRO', 'Livro/PDF'),
        ('OUTRO', 'Outro'),
    ]

    curso = models.ForeignKey(
        Curso, 
        on_delete=models.CASCADE, 
        related_name='materiais_complementares'
    )
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='VIDEO')
    link = models.URLField(max_length=200)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.titulo