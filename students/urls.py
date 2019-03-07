from django.urls import path

from .views import StudentCreateView
from .views import StudentDeleteView
from .views import StudentDetailView
from .views import StudentUpdateView


prefix = 'cursos/<int:classroom_pk>/estudiantes'


urlpatterns = [
    path(
        f'{prefix}/crear/',
        StudentCreateView.as_view(),
        name='student-create',
    ),

    path(
        f'{prefix}/<int:pk>/',
        StudentDetailView.as_view(),
        name='student-detail',
    ),

    path(
        f'{prefix}/<int:pk>/editar/',
        StudentUpdateView.as_view(),
        name='student-update',
    ),

    path(
        f'{prefix}/<int:pk>/eliminar/',
        StudentDeleteView.as_view(),
        name='student-delete',
    ),
]
