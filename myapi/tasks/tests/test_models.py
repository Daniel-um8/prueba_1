from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Task, Etiqueta

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.etiqueta = Etiqueta.objects.create(nombre="Urgente")

    def test_create_task(self):
        task = Task.objects.create(
            title="Tarea de prueba",
            description="Descripción de prueba",
            completed=False,
            user=self.user
        )
        task.etiquetas.add(self.etiqueta)
        self.assertEqual(task.title, "Tarea de prueba")
        self.assertEqual(task.description, "Descripción de prueba")
        self.assertFalse(task.completed)
        self.assertEqual(task.user, self.user)
        self.assertIn(self.etiqueta, task.etiquetas.all())