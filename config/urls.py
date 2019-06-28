import os

from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from graphene_django.views import GraphQLView

from .views import index


urlpatterns = [
    path('', include('users.urls')),
    path('', index, name='index'),
    path('', include('events.urls')),
    path('', include('parents.urls')),
    path('', include('posts.urls')),
    path('', include('questions.urls')),
    path('', include('students.urls')),
    path('cursos/', include('classrooms.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('graphql/', GraphQLView.as_view(graphiql=settings.DEBUG)),
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
