import pytest
from rest_framework.test import APIClient
from clinica.models import Dentista, Clinica
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_list_dentistas():
    clinica = Clinica.objects.create(
        nombre="Clinica Central",
        direccion="Av 123",
        telefono="111222",
        email="central@mail.com",
        sede="Lima"
    )

    Dentista.objects.create(
        nombre="Dr. Mario",
        dni="12345678",
        telefono="987654321",
        email="mario@mail.com",
        clinica=clinica
    )

    client = APIClient()
    user = User.objects.create_user(username="al", password="123")
    client.force_authenticate(user)

    response = client.get("/api/clinica/dentistas/")

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["nombre"] == "Dr. Mario"


@pytest.mark.django_db
def test_create_dentista():
    clinica = Clinica.objects.create(
        nombre="Clinica Norte",
        direccion="Av Norte",
        telefono="999",
        email="norte@mail.com",
        sede="Lima"
    )

    client = APIClient()
    user = User.objects.create_user(username="al", password="123")
    client.force_authenticate(user)

    data = {
        "nombre": "Dra. Ana",
        "dni": "87654321",
        "telefono": "900111222",
        "email": "ana@mail.com",
        "clinica_id": clinica.id   
    }


    response = client.post("/api/clinica/dentistas/", data, format="json")

    assert response.status_code == 201
    assert response.data["nombre"] == "Dra. Ana"
    assert response.data["clinica"]["id"] == clinica.id


@pytest.mark.django_db
def test_update_dentista():
    clinica = Clinica.objects.create(
        nombre="Clinica Sur",
        direccion="Av Sur",
        telefono="555",
        email="sur@mail.com",
        sede="Lima"
    )

    dentista = Dentista.objects.create(
        nombre="Dr. Luis",
        dni="11223344",
        telefono="777888",
        email="luis@mail.com",
        clinica=clinica
    )

    client = APIClient()
    user = User.objects.create_user(username="al", password="123")
    client.force_authenticate(user)

    data = {"nombre": "Dr. Luis Actualizado"}

    response = client.patch(f"/api/clinica/dentistas/{dentista.id}/", data, format="json")

    assert response.status_code == 200
    assert response.data["nombre"] == "Dr. Luis Actualizado"


@pytest.mark.django_db
def test_delete_dentista():
    clinica = Clinica.objects.create(
        nombre="Clinica Oeste",
        direccion="Av Oeste",
        telefono="444",
        email="oeste@mail.com",
        sede="Lima"
    )

    dentista = Dentista.objects.create(
        nombre="Dr. Beto",
        dni="55667788",
        telefono="111222",
        email="beto@mail.com",
        clinica=clinica
    )

    client = APIClient()
    user = User.objects.create_user(username="al", password="123")
    client.force_authenticate(user)

    response = client.delete(f"/api/clinica/dentistas/{dentista.id}/")

    assert response.status_code == 204
    assert Dentista.objects.count() == 0
