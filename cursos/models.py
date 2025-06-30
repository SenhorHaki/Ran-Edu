from django.db import models
from django.conf import settings

class Curso(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    carga_horaria = models.IntegerField()
    alunos = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Inscricao', related_name='cursos_inscritos', blank=True)
    def __str__(self): return self.titulo

class Modulo(models.Model):
    curso = models.ForeignKey(Curso, related_name='modulos', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    ordem = models.PositiveIntegerField()
    class Meta: ordering = ['ordem']
    def __str__(self): return f"{self.curso.titulo} - Módulo {self.ordem}: {self.titulo}"

class Aula(models.Model):
    modulo = models.ForeignKey(Modulo, related_name='aulas', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    ordem = models.PositiveIntegerField()
    video_url = models.URLField(max_length=200, blank=True, null=True)
    class Meta: ordering = ['ordem']
    def __str__(self): return f"Aula {self.ordem}: {self.titulo}"

class Inscricao(models.Model):
    aluno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    data_inscricao = models.DateTimeField(auto_now_add=True)
    progresso = models.IntegerField(default=0)
    class Meta: unique_together = [['aluno', 'curso']]
    def __str__(self): return f"{self.aluno.username} inscrito em {self.curso.titulo}"

class AulaConcluida(models.Model):
    aluno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    data_conclusao = models.DateTimeField(auto_now_add=True)
    class Meta: unique_together = [['aluno', 'aula']]
    def __str__(self): return f"{self.aluno.username} concluiu {self.aula.titulo}"

class Postagem(models.Model):
    """
    Representa um tópico de discussão (post) criado por um usuário dentro de um curso.
    """
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='postagens')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    """
    Represents a comment in response to a Post.
    """
    postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_edicao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comentário de {self.autor.username} em "{self.postagem.titulo}"'
    
