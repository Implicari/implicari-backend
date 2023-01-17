from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path


urlpatterns: list = [
    # path('', include('users.urls')),
    # path('', index, name='index'),
    # path('', include('events.urls')),
    # path('', include('parents.urls')),
    # path('', include('posts.urls')),
    # path('', include('questions.urls')),
    # path('', include('students.urls')),
    # path('', include('evaluations.urls')),
    # path('', include('django.contrib.auth.urls')),
    # path('cursos/', include('classrooms.urls')),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
