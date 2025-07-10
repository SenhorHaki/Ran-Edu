from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Recurso
from .forms import RecursoForm
from .permissions import IsProfessor 

class BibliotecaView(LoginRequiredMixin, View):
    login_url = '/admin/login/'
    form_class = RecursoForm
    template_name = 'biblioteca/lista_recursos.html'

    def get(self, request):
        form = self.form_class()
        recursos = Recurso.objects.all()
        return render(request, self.template_name, {'form': form, 'recursos': recursos})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            recurso = form.save(commit=False)
            recurso.autor = request.user
            recurso.save()
            return redirect('biblioteca:lista-recursos')

        recursos = Recurso.objects.all()
        return render(request, self.template_name, {'form': form, 'recursos': recursos})