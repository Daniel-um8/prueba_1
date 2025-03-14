from rest_framework.test import APITestCase
from ..models import Task, Etiqueta
from ..serializers import TaskSerializer
from django.contrib.auth.models import User
from datetime import date, timedelta

class SerializerTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.etiqueta = Etiqueta.objects.create(nombre="Urgente")

    def test_task_serializer(self):
        data = {
            "title": "Tarea de prueba",
            "description": "Descripción de prueba",
            "completed": False,
            "fecha_vencimiento": "2025-12-31",
            "etiquetas": [self.etiqueta.id]
        }
        serializer = TaskSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        task = serializer.save(user=self.user)
        self.assertEqual(task.title, "Tarea de prueba")
        self.assertEqual(task.etiquetas.first(), self.etiqueta)

    def test_task_serializer_invalid_date(self):
        data = {
            "title": "Tarea de prueba",
            "description": "Descripción de prueba",
            "completed": False,
            "fecha_vencimiento": "2020-01-01",
            "etiquetas": [self.etiqueta.id]
        }
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("fecha_vencimiento", serializer.errors)