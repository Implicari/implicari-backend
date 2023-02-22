from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from rest_framework.authtoken import views


urlpatterns: list = [
    path('admin/', admin.site.urls),
    path('api/', include('implicari.apps.users.urls')),
    path('api/', include('implicari.apps.courses.urls')),
]

