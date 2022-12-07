from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

# Collection of URLs related to API (V2)
apiv2patterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redocs/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('auth/', include('auth_guard.urls')),
    path('users/', include('accounts.urls')),
]

# Collection of common URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(apiv2patterns)),
]


if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
