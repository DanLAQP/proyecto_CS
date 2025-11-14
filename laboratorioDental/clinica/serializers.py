from rest_framework import serializers
from .models import Clinica, Dentista

class ClinicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinica
        fields = '__all__'


class DentistaSerializer(serializers.ModelSerializer):

    # Mostrar datos completos de la clínica
    clinica = ClinicaSerializer(read_only=True)

    # Para escribir el ID de la clínica
    clinica_id = serializers.PrimaryKeyRelatedField(
        queryset=Clinica.objects.all(),
        source='clinica',          # asigna al campo real "clinica"
        write_only=True
    )

    class Meta:
        model = Dentista
        fields = [
            'id',
            'nombre',
            'dni',
            'telefono',
            'email',
            'clinica',      # lectura
            'clinica_id',   # escritura
            'created',
            'modified'
        ]
