import os

from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.urls import path

from .views import index
from .views import signin
from .views import SchoolListView


urlpatterns = [
    path('', index, name='index'),
    path('', include('users.urls')),
    path('signin/', signin, name='signin'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('schools/', SchoolListView.as_view(), name='school-list'),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    if os.environ.get('DEBUG_TOOLBAR', False):
        import debug_toolbar

        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

    else:
        pass

else:
    pass
