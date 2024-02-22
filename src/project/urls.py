from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

DEBUG = settings.DEBUG

urlpatterns = [
    path("favicon.ico", RedirectView.as_view(url="/static/images/icons/favicon.ico")),
    path("admin/", admin.site.urls),
    path("greetings/", include("greetings.urls")),
]

# for development environment only
if DEBUG:
    #  Django debug toolbar
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    # Serving static files from STATIC_ROOT folder
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # Serving media files uploaded by a user during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
