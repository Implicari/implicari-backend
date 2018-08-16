from django.urls import path

from .views import PostCreateView
from .views import PostDeleteView
from .views import PostDetailView
from .views import PostListView
from .views import PostUpdateView


prefix = 'cursos/<int:classroom_pk>/mesnajes'


urlpatterns = [
    path(f'{prefix}/', PostListView.as_view(), name='post-list'),

    path(
        f'{prefix}/crear/',
        PostCreateView.as_view(),
        name='post-create',
    ),

    path(
        f'{prefix}/<int:pk>/',
        PostDetailView.as_view(),
        name='post-detail',
    ),

    path(
        f'{prefix}/<int:pk>/editar',
        PostUpdateView.as_view(),
        name='post-update',
    ),

    path(
        f'{prefix}/<int:pk>/eliminar/',
        PostDeleteView.as_view(),
        name='post-delete',
    ),
]
