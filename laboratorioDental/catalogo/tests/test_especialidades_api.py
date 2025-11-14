import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from catalogo.models import Especialidad

User = get_user_model()


@pytest.mark.django_db
def test_list_especialidades():
    Especialidad.objects.create(nombre="Ortodoncia")
    Especialidad.objects.create(nombre="Implantología")

    user = User.objects.create_user(username="al", password="123")

    client = APIClient()
    client.force_authenticate(user)

    response = client.get("/api/catalogo/especialidades/")

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]["nombre"] == "Ortodoncia"


@pytest.mark.django_db
def test_create_especialidad():
    client = APIClient()
    user = User.objects.create_user(username="al", password="123")
    client.force_authenticate(user)

    data = {
        "nombre": "Prótesis"
    }

    response = client.post("/api/catalogo/especialidades/", data, format="json")

    assert response.status_code == 201
    assert response.data["nombre"] == "Prótesis"


@pytest.mark.django_db
def test_update_especialidad():
    especialidad = Especialidad.objects.create(nombre="Endodoncia")

    user = User.objects.create_user(username="al", password="123")
    client = APIClient()
    client.force_authenticate(user)

    response = client.patch(
        f"/api/catalogo/especialidades/{especialidad.id}/",
        {"nombre": "Endodoncia Avanzada"},
        format="json"
    )

    assert response.status_code == 200
    assert response.data["nombre"] == "Endodoncia Avanzada"


@pytest.mark.django_db
def test_delete_especialidad():
    especialidad = Especialidad.objects.create(nombre="Radiología")

    user = User.objects.create_user(username="al", password="123")
    client = APIClient()
    client.force_authenticate(user)

    response = client.delete(f"/api/catalogo/especialidades/{especialidad.id}/")

    assert response.status_code == 204
    assert Especialidad.objects.count() == 0
