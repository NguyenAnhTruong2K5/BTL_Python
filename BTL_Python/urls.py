from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Các app
    path('accounts/', include('Apps.Accounts.urls')),
    path('billings/', include('Apps.Billings.urls')),
    path('parkings/', include('Apps.Parkings.urls', namespace='Parkings')),
]

# Cho phép truy cập file media (ảnh check-in)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)