from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Especialidad, SubEspecialidad
from .serializers import EspecialidadSerializer, SubEspecialidadSerializer

class EspecialidadViewSet(viewsets.ModelViewSet):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer
    permission_classes = [permissions.IsAuthenticated]


class SubEspecialidadViewSet(viewsets.ModelViewSet):
    queryset = SubEspecialidad.objects.select_related('especialidad')
    serializer_class = SubEspecialidadSerializer
    permission_classes = [permissions.IsAuthenticated]
