from rest_framework import generics, permissions
from .serializers import UsuarioSerializer
from .models import Usuario
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm

class CriarUsuarioView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.AllowAny]

class MeView(APIView):
    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)

class LoginView(View):
    form_class = LoginForm
    template_name = 'usuarios/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('dashboard:home')
        
        contexto = {'form': form, 'error_message': 'Usuário ou senha inválidos.'}
        return render(request, self.template_name, contexto)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('usuarios:login')