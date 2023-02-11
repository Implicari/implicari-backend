from django.urls import include, path

from implicari.config.urls import urlpatterns


urlpatterns += [
    path('__debug__/', include('debug_toolbar.urls')),
]
