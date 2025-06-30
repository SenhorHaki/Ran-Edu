from django.db import models
from django.conf import settings

class Conquista(models.Model):
    """
    Define uma medalha ou conquista que um aluno pode ganhar.
    Ex: "Primeiros Passos", "Mestre do Módulo de Python", etc.
    """
    nome = models.CharField(max_length=100)
    descricao = models.TextField(help_text="Explique o que o aluno precisa fazer para ganhar.")
    # Usaremos os nomes das classes do Font Awesome para os ícones
    icone = models.CharField(max_length=50, help_text="ex: fas fa-star, fas fa-trophy")

    def __str__(self):
        return self.nome

class ConquistaDoAluno(models.Model):
    """
    Registra que um aluno específico ganhou uma conquista específica.
    É a "ponte" entre Alunos e Conquistas.
    """
    aluno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conquistas')
    conquista = models.ForeignKey(Conquista, on_delete=models.CASCADE)
    data_obtencao = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Impede que um aluno ganhe a mesma conquista duas vezes.
        unique_together = [['aluno', 'conquista']]

    def __str__(self):
        return f"{self.aluno.username} ganhou '{self.conquista.nome}'"