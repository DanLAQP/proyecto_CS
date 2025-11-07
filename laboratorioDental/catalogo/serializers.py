from rest_framework import serializers
from .models import Especialidad, SubEspecialidad

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = '__all__'


class SubEspecialidadSerializer(serializers.ModelSerializer):
    especialidad = EspecialidadSerializer(read_only=True)

    class Meta:
        model = SubEspecialidad
        fields = '__all__'
