from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from Apps.Parkings import views as parking_views

urlpatterns = [
    # Home
    path('', parking_views.index, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include("Apps.Accounts.urls")),  # Template URLs
    path('api/accounts/', include("Apps.Accounts.api_urls")),  # API URLs
    path('parkings/', include("Apps.Parkings.urls", namespace='Parkings')),
    # Billing endpoints (templates / api) - included so homepage links work
    # path('billings/', include("Apps.Billings.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
