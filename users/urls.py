from django.urls import path

from .views import signup
from .views import ProfileUpdateView
from .views import UserUpdateView
from .views import UserDetailView


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('perfil/', ProfileUpdateView.as_view(), name='profile'),

    path('usuarios/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('usuarios/<int:pk>/editar', UserUpdateView.as_view(), name='user-update'),
]
