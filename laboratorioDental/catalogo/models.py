from django.db import models

# Create your models here.

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class SubEspecialidad(models.Model):
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, related_name='subespecialidades')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.especialidad.nombre})"
