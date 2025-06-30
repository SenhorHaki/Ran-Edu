from rest_framework import generics, permissions
from .serializers import UsuarioSerializer
from .models import Usuario
from rest_framework.views import APIView
from rest_framework.response import Response


class CriarUsuarioView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.AllowAny]


class MeView(APIView):
    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)