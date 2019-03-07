from django.urls import path

from .views import PostCreateView
from .views import PostDetailView
from .views import PostListView


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
]
