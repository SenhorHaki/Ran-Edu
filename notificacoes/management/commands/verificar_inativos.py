from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from cursos.models import Inscricao, AulaConcluida
from usuarios.models import Usuario
from notificacoes.models import Notificacao

class Command(BaseCommand):
    help = 'Verifica alunos inativos e gera notificações para os professores.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando verificação de alunos inativos...'))
        
        # Define o que consideramos "inatividade" (ex: 7 dias)
        #limite_inatividade = timezone.now() - timedelta(days=7)
        limite_inatividade = timezone.now() - timedelta(seconds=0)

        # Encontra inscrições ativas (progresso entre 1 e 99)
        inscricoes_ativas = Inscricao.objects.filter(progresso__gt=0, progresso__lt=100)
        
        alunos_notificados = []

        for inscricao in inscricoes_ativas:
            # Encontra a data da última aula concluída pelo aluno naquele curso
            ultima_aula_concluida = AulaConcluida.objects.filter(
                aluno=inscricao.aluno,
                aula__modulo__curso=inscricao.curso
            ).order_by('-data_conclusao').first()

            # Se o aluno já concluiu alguma aula e a última foi há mais de 7 dias...
            if ultima_aula_concluida and ultima_aula_concluida.data_conclusao < limite_inatividade:
                # Lógica para encontrar o professor (por enquanto, vamos notificar o admin)
                # No futuro, o curso teria um campo 'professor'
                admin_user = Usuario.objects.filter(is_superuser=True).first()
                
                if admin_user:
                    mensagem = (
                        f"O aluno '{inscricao.aluno.username}' parece estar inativo no curso "
                        f"'{inscricao.curso.titulo}'. Sua última atividade foi há mais de 7 dias."
                    )
                    
                    # Cria a notificação para o admin/professor
                    Notificacao.objects.get_or_create(
                        destinatario=admin_user,
                        mensagem=mensagem
                    )
                    alunos_notificados.append(inscricao.aluno.username)

        if alunos_notificados:
            self.stdout.write(self.style.SUCCESS(f'Notificações geradas para os alunos: {", ".join(set(alunos_notificados))}'))
        else:
            self.stdout.write(self.style.SUCCESS('Nenhum aluno inativo encontrado.'))
