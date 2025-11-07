from rest_framework import serializers
from .models import Orden, OrdenEspecial, Cita

class OrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orden
        fields = '__all__'


class OrdenEspecialSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenEspecial
        fields = '__all__'


class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = '__all__'
