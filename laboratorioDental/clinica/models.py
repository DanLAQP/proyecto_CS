from django.db import models

# Create your models here.

class Clinica(models.Model):
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)  
    email = models.EmailField()
    sede = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Dentista(models.Model):
    nombre = models.CharField(max_length=150)
    dni = models.CharField(max_length=15)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    clinica = models.ForeignKey(Clinica, on_delete=models.CASCADE, related_name='dentistas')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
