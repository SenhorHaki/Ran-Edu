from django.urls import reverse, NoReverseMatch
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.urls import reverse

def custom_404_view(request, exception):
    # Retorna uma resposta de texto simples para o teste
    return HttpResponseNotFound("<h1>Teste de Erro 404 Customizado Funcionando!</h1>")