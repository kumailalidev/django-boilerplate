from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

DEBUG = settings.DEBUG

urlpatterns = [
    # Favicon
    path("favicon.ico", RedirectView.as_view(url="/static/images/icons/favicon.ico")),
    # Django Admin
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("accounts/", include("project.accounts.urls", namespace="accounts")),
    # Project
    path("greetings/", include("project.greetings.urls")),
    # Media files
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# for development environment only
if DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            path("__debug__/", include(debug_toolbar.urls)),
        ]
