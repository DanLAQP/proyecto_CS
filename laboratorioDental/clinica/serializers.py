from rest_framework import serializers
from .models import Clinica, Dentista

class ClinicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinica
        fields = '__all__'


class DentistaSerializer(serializers.ModelSerializer):
    clinica = ClinicaSerializer(read_only=True)

    class Meta:
        model = Dentista
        fields = '__all__'
