from django.urls import path

from .views import ObtainAuthToken, UserProfileView


app_name = 'users'


urlpatterns = [
    path('auth/', ObtainAuthToken.as_view(), name='auth'),
    path('profile/', UserProfileView.as_view()),
]
