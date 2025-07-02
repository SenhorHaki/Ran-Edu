from django.urls import path
from .views import PortalResponsavelView

urlpatterns = [
    path('meus-alunos/', PortalResponsavelView.as_view(), name='portal-meus-alunos'),
]