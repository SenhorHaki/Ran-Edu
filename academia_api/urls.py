from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/cursos/', include('cursos.urls')),
    path('api/auth/', include('usuarios.urls')),
    path('api/gamificacao/', include('gamificacao.urls')),
    path('api/avaliacoes/', include('avaliacoes.urls')),
    path('api/portal-responsavel/', include('portal_responsavel.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/notificacoes/', include('notificacoes.urls')),
    path('api/recomendacoes/', include('recomendacoes.urls')),
    path('api/biblioteca/', include('biblioteca.urls')), 
    path('api/agendamento/', include('agendamento.urls')),   
    path('api/digitacao/', include('digitacao.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    