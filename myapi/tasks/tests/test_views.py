from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Task, Etiqueta

class ViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.etiqueta = Etiqueta.objects.create(nombre="Urgente")
        self.client.force_authenticate(user=self.user)

    def test_create_task(self):
        url = reverse('task-list-create')
        data = {
            "title": "Tarea de prueba",
            "description": "Descripción de prueba",
            "completed": False,
            "fecha_vencimiento": "2025-12-31",
            "etiquetas": [self.etiqueta.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, "Tarea de prueba")

    def test_get_task_list(self):
        Task.objects.create(
            title="Tarea de prueba",
            description="Descripción de prueba",
            completed=False,
            user=self.user
        )
        url = reverse('task-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Tarea de prueba")