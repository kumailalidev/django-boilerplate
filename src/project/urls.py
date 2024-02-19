from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

DEBUG = settings.DEBUG

urlpatterns = [
    path("admin/", admin.site.urls),
    path("greetings/", include("greetings.urls")),
]

# for development environment only
if DEBUG:
    #  Django debug toolbar
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    # Serving media files uploaded by a user during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
