from django.urls import path
from .views import PortalView

app_name = 'portal_responsavel'

urlpatterns = [
    path('', PortalView.as_view(), name='portal'),
]