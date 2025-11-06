from django.db import models

# Create your models here.
from accounts.models import Usuario, Tecnico
from clinica.models import Dentista
from catalogo.models import Especialidad, SubEspecialidad

class Orden(models.Model):
    nombrePaciente = models.CharField(max_length=150)
    dentista = models.ForeignKey(Dentista, on_delete=models.CASCADE, related_name='ordenes')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='ordenes_usuario')
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE, related_name='ordenes_tecnico')
    fechaRecepcion = models.DateTimeField()
    fechaEntrega = models.DateTimeField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    acuenta = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50)
    detalleTrabajo = models.TextField(blank=True)
    cubeta = models.CharField(max_length=50, blank=True)
    stl = models.CharField(max_length=50, blank=True)
    rMordida = models.CharField(max_length=50, blank=True)
    antagonista = models.CharField(max_length=50, blank=True)
    grafico1 = models.IntegerField(null=True, blank=True)
    grafico2 = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Orden #{self.id} - {self.nombrePaciente}"


class OrdenEspecial(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='especiales')
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    subespecialidad = models.ForeignKey(SubEspecialidad, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Especial de {self.orden}"


class Cita(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='citas')
    descripcion = models.TextField(blank=True)
    fechaEntrega = models.DateTimeField()
    estado = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cita {self.id} ({self.estado})"
