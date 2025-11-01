from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from .models import Usuario, AppSingleton
import logging

logger = logging.getLogger(__name__)

# Login para todos los usuarios
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)  # inicia la sesión
            # Usar el singleton para llevar un contador de logins
            try:
                cfg = AppSingleton.load()
                cfg.increment_logins(1)
                logger.info(f"Incremented AppSingleton.login_count -> {cfg.login_count}")
            except Exception:
                # No queremos bloquear el login por fallos en el singleton
                logger.exception("Error updating AppSingleton")

            return Response({
                "message": "Login exitoso",
                "username": user.username,
                "rol": user.rol,
                "is_staff": user.is_staff,
                "app_singleton": {
                    "site_name": cfg.site_name if 'cfg' in locals() else None,
                    "login_count": cfg.login_count if 'cfg' in locals() else None,
                }
            })
        else:
            return Response(
                {"error": "Credenciales incorrectas"},
                status=status.HTTP_401_UNAUTHORIZED
            )

# Crear usuarios (solo admins) usando APIView
class CreateUserView(APIView):
    permission_classes = []  # solo admins pueden acceder

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        rol = request.data.get('rol')

        if not username or not password or not rol:
            return Response({"error": "Faltan datos"}, status=status.HTTP_400_BAD_REQUEST)

        if Usuario.objects.filter(username=username).exists():
            return Response({"error": "Usuario ya existe"}, status=status.HTTP_400_BAD_REQUEST)

        user = Usuario.objects.create_user(username=username, password=password, rol=rol)
        user.save()
        return Response({"message": f"Usuario {username} creado con rol {rol}"}, status=status.HTTP_201_CREATED)


class AppSingletonView(APIView):
    """Read-only endpoint to fetch the current AppSingleton state.

    This endpoint forces a DB refresh so clients always get the latest value
    (useful when multiple processes may update the singleton).
    """

    permission_classes = []

    def get(self, request):
        try:
            cfg = AppSingleton.load(force_refresh=True)
            return Response({
                "site_name": cfg.site_name,
                "login_count": cfg.login_count,
                "updated": cfg.updated,
            })
        except Exception:
            logger.exception("Error loading AppSingleton")
            return Response({"error": "Could not load app singleton"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
