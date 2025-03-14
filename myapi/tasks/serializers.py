from rest_framework import serializers
from .models import Task, Etiqueta
from datetime import date
from drf_spectacular.utils import extend_schema_field

class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etiqueta
        fields = ['id', 'nombre']

class TaskSerializer(serializers.ModelSerializer):
    etiquetas = serializers.PrimaryKeyRelatedField(queryset=Etiqueta.objects.all(), many=True)  # Campo escribible
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'fecha_vencimiento', 'user', 'etiquetas']  # Ahora 'user' está incluido
        extra_kwargs = {
            'user': {'read_only': True}  # Hace que el campo 'user' sea de solo lectura
        }

    @extend_schema_field(str)
    def get_title(self, obj):
        return obj.title

    # Validación básica: El título no puede estar vacío y debe tener al menos 5 caracteres.
    title = serializers.CharField(required=True, min_length=5)

    # Validación básica: La descripción no puede estar vacía.
    description = serializers.CharField(required=True)

    # Validación personalizada: El título no puede contener palabras prohibidas.
    def validate_title(self, value):
        palabras_prohibidas = ['spam', 'publicidad', 'oferta']
        for palabra in palabras_prohibidas:
            if palabra in value.lower():
                raise serializers.ValidationError(f"El título no puede contener la palabra '{palabra}'.")
        return value
    
    # Validación personalizada: La fecha de vencimiento no puede ser en el pasado.
    def validate_fecha_vencimiento(self, value):
        if value and value < date.today():  # Asegúrate de que value sea de tipo date
            raise serializers.ValidationError("La fecha de vencimiento no puede ser en el pasado.")
        return value