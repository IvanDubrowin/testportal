from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from testportal import settings
from portal.admin import admin_site


urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include(('portal.urls', 'portal'), namespace='portal')),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
