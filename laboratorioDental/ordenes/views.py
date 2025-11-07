from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Orden, OrdenEspecial, Cita
from .serializers import OrdenSerializer, OrdenEspecialSerializer, CitaSerializer

class OrdenViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrdenEspecialViewSet(viewsets.ModelViewSet):
    queryset = OrdenEspecial.objects.select_related('orden')
    serializer_class = OrdenEspecialSerializer
    permission_classes = [permissions.IsAuthenticated]


class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.select_related('orden')
    serializer_class = CitaSerializer
    permission_classes = [permissions.IsAuthenticated]
