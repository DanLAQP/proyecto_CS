from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EspecialidadViewSet, SubEspecialidadViewSet

router = DefaultRouter()
router.register(r'especialidades', EspecialidadViewSet)
router.register(r'subespecialidades', SubEspecialidadViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
