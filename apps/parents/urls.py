from django.urls import path

from .views import ParentCreateView
from .views import ParentDetailView


prefix = 'cursos/<int:classroom_pk>/estudiantes/<int:student_pk>/apoderados'


urlpatterns = [

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

]
