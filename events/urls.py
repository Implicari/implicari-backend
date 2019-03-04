from django.urls import path

from .views import EventCreateView
from .views import EventDeleteView
from .views import EventDetailView
from .views import EventListView
from .views import EventUpdateView


prefix = 'cursos/<int:classroom_pk>/eventos'


urlpatterns = [
    path(f'{prefix}/', EventListView.as_view(), name='event-list'),

    path(
        f'{prefix}/crear/',
        EventCreateView.as_view(),
        name='event-create',
    ),

    path(
        f'{prefix}/<int:pk>/',
        EventDetailView.as_view(),
        name='event-detail',
    ),

    path(
        f'{prefix}/<int:pk>/editar',
        EventUpdateView.as_view(),
        name='event-update',
    ),

    path(
        f'{prefix}/<int:pk>/eliminar/',
        EventDeleteView.as_view(),
        name='event-delete',
    ),
]
