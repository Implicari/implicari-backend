from django.urls import path

from .views import ParentCreateView
from .views import ParentDeleteView
from .views import ParentDetailView
from .views import ParentListView
from .views import ParentUpdateView


prefix = 'cursos/<int:classroom_pk>/estudiantes/<int:student_pk>/apoderados'


urlpatterns = [
    path(f'{prefix}/', ParentListView.as_view(), name='parent-list'),

    path(
        f'{prefix}/crear/',
        ParentCreateView.as_view(),
        name='parent-create',
    ),

    path(
        f'{prefix}/<int:pk>/',
        ParentDetailView.as_view(),
        name='parent-detail',
    ),

    path(
        f'{prefix}/<int:pk>/editar',
        ParentUpdateView.as_view(),
        name='parent-update',
    ),

    path(
        f'{prefix}/<int:pk>/eliminar/',
        ParentDeleteView.as_view(),
        name='parent-delete',
    ),
]
