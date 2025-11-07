from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Clinica, Dentista
from .serializers import ClinicaSerializer, DentistaSerializer

class ClinicaViewSet(viewsets.ModelViewSet):
    queryset = Clinica.objects.all()
    serializer_class = ClinicaSerializer
    permission_classes = [permissions.IsAuthenticated]


class DentistaViewSet(viewsets.ModelViewSet):
    queryset = Dentista.objects.select_related('clinica')
    serializer_class = DentistaSerializer
    permission_classes = [permissions.IsAuthenticated]
