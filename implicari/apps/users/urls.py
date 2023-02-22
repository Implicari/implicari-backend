from django.urls import path

from .views import ObtainAuthToken


app_name = 'users'


urlpatterns = [
    path('auth/', ObtainAuthToken.as_view(), name='auth'),
]
