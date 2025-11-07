from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClinicaViewSet, DentistaViewSet

router = DefaultRouter()
router.register(r'clinicas', ClinicaViewSet)
router.register(r'dentistas', DentistaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
