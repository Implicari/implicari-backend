from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from implicari.config.urls import urlpatterns


schema_view = get_schema_view(
   openapi.Info(
      title="Implicari API",
      default_version='v1',
   ),
   public=False,
   permission_classes=[permissions.IsAdminUser],
)


urlpatterns += [
    path('__debug__/', include('debug_toolbar.urls')),

    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
