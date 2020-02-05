from django.urls import path

from .views import QuestionCreateView
from .views import QuestionDetailView
from .views import QuestionListView


prefix = 'cursos/<int:classroom_pk>/preguntas'


urlpatterns = [
    path(f'{prefix}/', QuestionListView.as_view(), name='question-list'),

    path(
        f'{prefix}/crear/',
        QuestionCreateView.as_view(),
        name='question-create',
    ),

    path(
        f'{prefix}/<int:pk>/',
        QuestionDetailView.as_view(),
        name='question-detail',
    ),
]
