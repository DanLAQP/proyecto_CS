from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('tecnico', 'Técnico'),
        ('recepcionista', 'Recepcionista'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='recepcionista')

    def __str__(self):
        return self.username
