import pytest
from rest_framework.test import APIClient
from clinica.models import Clinica
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_list_clinicas():
    Clinica.objects.create(
        nombre="Clinica 1",
        direccion="Av 1",
        telefono="123",
        email="c1@mail.com",
        sede="Lima"
    )

    client = APIClient()
    user = User.objects.create_user(username="al", password="123")
    client.force_authenticate(user=user)

    response = client.get("/api/clinica/clinicas/")
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_create_clinica_api():
    client = APIClient()
    user = User.objects.create_user(username="al", password="123")
    client.force_authenticate(user=user)

    data = {
        "nombre": "Nueva Clinica",
        "direccion": "Av Siempre Viva",
        "telefono": "987654321",
        "email": "new@mail.com",
        "sede": "San Isidro"
    }

    response = client.post("/api/clinica/clinicas/", data, format="json")

    assert response.status_code == 201
    assert response.data["nombre"] == "Nueva Clinica"


@pytest.mark.django_db
def test_update_clinica_api():
    clinica = Clinica.objects.create(
        nombre="Antigua",
        direccion="Av 100",
        telefono="111",
        email="old@mail.com",
        sede="Lima"
    )

    client = APIClient()
    user = User.objects.create_user(username="al", password="123")
    client.force_authenticate(user=user)

    data = {"nombre": "Actualizada"}

    response = client.patch(f"/api/clinica/clinicas/{clinica.id}/", data, format="json")

    assert response.status_code == 200
    assert response.data["nombre"] == "Actualizada"


@pytest.mark.django_db
def test_delete_clinica_api():
    clinica = Clinica.objects.create(
        nombre="Clinica X",
        direccion="Calle X",
        telefono="555",
        email="x@mail.com",
        sede="Lima"
    )

    client = APIClient()
    user = User.objects.create_user(username="al", password="123")
    client.force_authenticate(user=user)

    response = client.delete(f"/api/clinica/clinicas/{clinica.id}/")

    assert response.status_code == 204
    assert Clinica.objects.count() == 0
