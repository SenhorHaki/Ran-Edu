# Em academia_api/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import custom_404_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- PÁGINAS DA APLICAÇÃO WEB (prefixo /app/ ou /contas/) ---
    path('app/', include('dashboard.urls')),
    path('contas/', include('usuarios.urls')),
    path('app/cursos/', include('cursos.urls')),
    path('app/gamificacao/', include('gamificacao.urls')),
    path('app/avaliacoes/', include('avaliacoes.urls')),
    path('app/biblioteca/', include('biblioteca.urls')),
    path('app/agendamento/', include('agendamento.urls')),
    path('app/digitacao/', include('digitacao.urls')),
    path('app/recomendacoes/', include('recomendacoes.urls')),
    path('app/notificacoes/', include('notificacoes.urls')),
    path('app/portal-responsavel/', include('portal_responsavel.urls')),
    
    # --- ROTAS DA API (prefixo /api/) ---
    path('api/auth/', include('usuarios.urls_api')),
    path('api/cursos/', include('cursos.urls_api')),
    path('api/gamificacao/', include('gamificacao.urls_api')),
    path('api/avaliacoes/', include('avaliacoes.urls_api')),
    path('api/portal-responsavel/', include('portal_responsavel.urls_api')),
    path('api/notificacoes/', include('notificacoes.urls_api')),
    path('api/recomendacoes/', include('recomendacoes.urls_api')),
    path('api/biblioteca/', include('biblioteca.urls_api')),
    path('api/agendamento/', include('agendamento.urls_api')),
    path('api/digitacao/', include('digitacao.urls_api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
handler404 = 'academia_api.views.custom_404_view'