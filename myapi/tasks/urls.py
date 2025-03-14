from django.urls import path
from .views import TaskListCreate, debug_env
from.views import TaskRetrieveUpdateDestroy

urlpatterns = [
    path('tasks/', TaskListCreate.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroy.as_view(), name='task-detail'),
    path('debug-env/', debug_env, name='debug-env'),  # Ruta de depuración
]