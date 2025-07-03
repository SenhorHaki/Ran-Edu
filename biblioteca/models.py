from django.db import models
from django.conf import settings
from usuarios.models import Usuario 
from cursos.models import Curso 

class Recurso(models.Model):
    curso = models.ForeignKey(
        Curso, 
        on_delete=models.CASCADE, 
        related_name='recursos_biblioteca',
        null=True, 
        blank=True
    )

    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, 
        null=True,
        related_name='recursos_criados',
        limit_choices_to={'tipo': Usuario.TipoUsuario.PROFESSOR}
    )
    arquivo = models.FileField(upload_to='recursos_professores/')
    data_upload = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_upload']

    def __str__(self):
        return self.titulo