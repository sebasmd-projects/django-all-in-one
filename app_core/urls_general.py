from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

admin_url = settings.ADMIN_URL

handler400 = 'app_core.utils.views.handler400'

handler403 = 'app_core.utils.views.handler403'

handler404 = 'app_core.utils.views.handler404'

handler500 = 'app_core.utils.views.handler500'


# YASG schema view
schema_view = get_schema_view(
    openapi.Info(
        title='Backend EndPoints',
        default_version='v1.0.0',
        description='API documentation and endpoint representations',
        # TODO terms_of_service YASG
        # terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='contact@pymedesk.com'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Admin and debug urls
urlpatterns_general = [
    path(
        admin_url,
        admin.site.urls
    ),
    path(
        '__debug__/',
        include('debug_toolbar.urls')
    ),
]

# Django yet another swagger generator urls
urlpatterns_general += [
    path(
        'api/docs/',
        schema_view.with_ui(
            'swagger',
            cache_timeout=0
        ),
        name='schema-swagger-ui'
    ),
    path(
        'api/redocs/',
        schema_view.with_ui(
            'redoc',
            cache_timeout=0
        ),
        name='schema-redoc'
    ),
    path(
        'api/docs/<format>/',
        schema_view.without_ui(
            cache_timeout=0
        ),
        name='schema-json-yaml'
    ),
]

# Static files urls
urlpatterns_general += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)

# Media files urls
urlpatterns_general += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
