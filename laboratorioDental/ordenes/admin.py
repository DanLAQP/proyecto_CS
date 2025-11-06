from django.contrib import admin
from .models import Orden, OrdenEspecial, Cita
# Register your models here.


admin.site.register(Orden)
admin.site.register(OrdenEspecial)
admin.site.register(Cita)