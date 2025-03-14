from django.http import JsonResponse
from decouple import config
from django.db import connection
from rest_framework import generics, permissions
from .models import Task
from .serializers import TaskSerializer
from drf_spectacular.utils import extend_schema

class TaskListCreate(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description="Obtener una lista de tareas o crear una nueva tarea.",
        responses={200: TaskSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        description="Crear una nueva tarea.",
        request=TaskSerializer,
        responses={201: TaskSerializer},
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # Asigna el usuario autenticado al campo 'user'
        serializer.save(user=self.request.user)

class TaskRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

def debug_env(request):
    try:
        # Verificar la conexión a la base de datos
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_connection = "OK"
    except Exception as e:
        db_connection = str(e)

    return JsonResponse({
        'SECRET_KEY': config('SECRET_KEY'),
        'DB_NAME': config('DB_NAME'),
        'DB_USER': config('DB_USER'),
        'DB_CONNECTION': db_connection,  # Verificar la conexión a la base de datos
    })