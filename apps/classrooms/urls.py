from django.urls import path

from .views import ClassroomCreateView
from .views import ClassroomDeleteView
from .views import ClassroomDetailView
from .views import ClassroomListView
from .views import ClassroomUpdateView


urlpatterns = [
    path('', ClassroomListView.as_view(), name='classroom-list'),

    path(
        'crear/',
        ClassroomCreateView.as_view(),
        name='classroom-create',
    ),

    path(
        '<int:pk>/',
        ClassroomDetailView.as_view(),
        name='classroom-detail',
    ),

    path(
        '<int:pk>/editar/',
        ClassroomUpdateView.as_view(),
        name='classroom-update',
    ),

    path(
        '<int:pk>/eliminar/',
        ClassroomDeleteView.as_view(),
        name='classroom-delete',
    ),
]
