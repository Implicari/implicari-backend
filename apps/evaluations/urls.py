from django.urls import path

from .views import EvaluationCreateView
from .views import EvaluationDeleteView
from .views import EvaluationDetailView
from .views import EvaluationUpdateView


prefix = 'cursos/<int:classroom_pk>/evaluaciones'


urlpatterns = [
    path(
        f'{prefix}/crear/',
        EvaluationCreateView.as_view(),
        name='evaluation-create',
    ),

    path(
        f'{prefix}/<int:pk>/',
        EvaluationDetailView.as_view(),
        name='evaluation-detail',
    ),

    path(
        f'{prefix}/<int:pk>/editar/',
        EvaluationUpdateView.as_view(),
        name='evaluation-update',
    ),

    path(
        f'{prefix}/<int:pk>/eliminar/',
        EvaluationDeleteView.as_view(),
        name='evaluation-delete',
    ),
]
