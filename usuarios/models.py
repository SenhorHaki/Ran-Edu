from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):     
    class TipoUsuario(models.TextChoices):
        ALUNO = 'ALUNO', 'Aluno'
        RESPONSAVEL = 'RESPONSAVEL', 'Responsável'
        PROFESSOR = 'PROFESSOR', 'Professor'

    tipo = models.CharField(
        max_length=11,
        choices=TipoUsuario.choices,
        default=TipoUsuario.ALUNO
    )

class ResponsavelAluno(models.Model):    
    """
    Modelo 'ponte' que cria a relação entre um Responsável e um Aluno.
    """
    responsavel = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='alunos_associados',
        limit_choices_to={'tipo': Usuario.TipoUsuario.RESPONSAVEL}
    )
    aluno = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='responsaveis_associados',
        limit_choices_to={'tipo': Usuario.TipoUsuario.ALUNO}
    )

    class Meta:
        verbose_name = "Relação Responsável-Aluno"
        verbose_name_plural = "Relações Responsável-Aluno"
    
    def __str__(self):
        return f"{self.responsavel.username} é responsável por {self.aluno.username}"
    
    