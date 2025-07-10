from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notificacao
from .serializers import NotificacaoSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin






class NotificacaoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para visualizar e interagir com as notificações.
    'ReadOnly' significa que ele só permite listar e ver detalhes, não criar/apagar via API.
    """
    serializer_class = NotificacaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filtra para retornar apenas as notificações do destinatário
        que fez a requisição.
        """
        return Notificacao.objects.filter(destinatario=self.request.user)

    @action(detail=True, methods=['post'])
    def marcar_como_lida(self, request, pk=None):
        """
        Ação customizada para marcar uma notificação específica como lida.
        Ex: POST /api/notificacoes/5/marcar_como_lida/
        """
        notificacao = self.get_object() # Pega a notificação pelo ID da URL
        notificacao.lida = True
        notificacao.save()
        return Response({'status': 'notificação marcada como lida'})
    
class PainelAlertasView(LoginRequiredMixin, View):
    login_url = '/admin/login/'
    template_name = 'notificacoes/painel_alertas.html'

    def get(self, request):
        notificacoes = Notificacao.objects.filter(destinatario=request.user)
        contexto = { 'notificacoes': notificacoes }
        return render(request, self.template_name, contexto)

class MarcarAlertaComoLidoView(LoginRequiredMixin, View):
    login_url = '/admin/login/'

    def post(self, request, pk):
        notificacao = get_object_or_404(Notificacao, id=pk, destinatario=request.user)
        notificacao.lida = True
        notificacao.save()
        return redirect('notificacoes:painel-alertas')
