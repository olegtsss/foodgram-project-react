from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from emailcheck.constants import VERIFICATION_PREFIX

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path(f'{VERIFICATION_PREFIX}/', include('emailcheck.urls')),
]

# Роут для media
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
