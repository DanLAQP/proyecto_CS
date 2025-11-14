import pytest
from clinica.models import Clinica, Dentista

@pytest.mark.django_db
def test_create_clinica():
    clinica = Clinica.objects.create(
        nombre="Clinica Central",
        direccion="Av. Lima 123",
        telefono="987654321",
        email="central@correo.com",
        sede="Surco"
    )

    assert clinica.id is not None
    assert clinica.nombre == "Clinica Central"


@pytest.mark.django_db
def test_create_dentista():
    clinica = Clinica.objects.create(
        nombre="Clinica Dental",
        direccion="Calle 123",
        telefono="123456789",
        email="c@mail.com",
        sede="Miraflores"
    )

    dentista = Dentista.objects.create(
        nombre="Dr. Juan",
        dni="12345678",
        telefono="987654321",
        email="juan@mail.com",
        clinica=clinica
    )

    assert dentista.id is not None
    assert dentista.clinica == clinica
