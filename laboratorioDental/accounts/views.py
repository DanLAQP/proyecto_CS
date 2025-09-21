from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from .models import Usuario

# Login para todos los usuarios
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)  # inicia la sesión
            return Response({
                "message": "Login exitoso",
                "username": user.username,
                "rol": user.rol,
                "is_staff": user.is_staff,
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
