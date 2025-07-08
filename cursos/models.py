import uuid
from django.db import models
from django.conf import settings
from usuarios.models import Usuario

class Curso(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    carga_horaria = models.PositiveIntegerField()

    def __str__(self):
        return self.titulo

class Turma(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='turmas')
    nome = models.CharField(max_length=100, help_text="Ex: 'Turma 2025.1'")
    alunos = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='turmas_inscritas', blank=True)

    def __str__(self):
        return f"{self.nome} - {self.curso.titulo}"

class Modulo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='modulos')
    titulo = models.CharField(max_length=200)
    ordem = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.titulo} (Curso: {self.curso.titulo})"

class Aula(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='aulas')
    titulo = models.CharField(max_length=200)
    ordem = models.PositiveIntegerField()
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.titulo

class Postagem(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='postagens', null=True, blank=True)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='postagens', null=True, blank=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_edicao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='respostas')
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_edicao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comentário de {self.autor.username} em "{self.postagem.titulo}"'

class Inscricao(models.Model):
    aluno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    data_inscricao = models.DateTimeField(auto_now_add=True)
    progresso = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.aluno.username} inscrito em {self.curso.titulo}"

class AulaConcluida(models.Model):
    aluno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    data_conclusao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['aluno', 'aula']]

class Certificado(models.Model):
    inscricao = models.OneToOneField(Inscricao, on_delete=models.CASCADE, related_name='certificado')
    data_emissao = models.DateTimeField(auto_now_add=True)
    codigo_validacao = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"Certificado para {self.inscricao.aluno} no curso {self.inscricao.curso}"
    
