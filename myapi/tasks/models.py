from django.db import models
from django.contrib.auth.models import User

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    fecha_vencimiento = models.DateField(null=True, blank=True)  # Se agrega una nueva columna para la fecha de vencimiento
    # Relación con el modelo User de Django
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    etiquetas = models.ManyToManyField(Etiqueta, related_name='tasks', blank=True)  # Relación muchos a muchos

    def __str__(self):
        return self.title