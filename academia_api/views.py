from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.urls import reverse, NoReverseMatch


def custom_404_view(request, exception):
    site_map = []
    if request.user.is_authenticated:
        paginas = [
            ('dashboard:home', 'Dashboard'),
            ('cursos:selecao-forum', 'Fóruns'),
            ('agendamento:minha-agenda', 'Minha Agenda'),
            ('avaliacoes:boletim-web', 'Meu Boletim'),
            ('gamificacao:lista-conquistas', 'Minhas Conquistas'),
            ('biblioteca:lista-recursos', 'Biblioteca (Professores)'),
            ('cursos:lista-certificados', 'Meus Certificados'),
            ('digitacao:game-page', 'Game de Digitação'),
        ]

        for url_name, page_title in paginas:
            try:
                url = reverse(url_name)
                site_map.append({'nome': page_title, 'url': url})
            except NoReverseMatch:
                print(f"Aviso no handler404: A rota com o nome '{url_name}' não foi encontrada.")
                pass

    contexto = {'site_map': site_map}
    return render(request, '404.html', contexto, status=404)