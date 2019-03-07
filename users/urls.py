from django.urls import path

from .views import signup
from .views import ProfileUpdateView


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('perfil/', ProfileUpdateView.as_view(), name='profile'),
]
