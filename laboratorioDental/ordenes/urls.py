from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrdenViewSet, OrdenEspecialViewSet, CitaViewSet

router = DefaultRouter()
router.register(r'ordenes', OrdenViewSet)
router.register(r'ordenes-especiales', OrdenEspecialViewSet)
router.register(r'citas', CitaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
