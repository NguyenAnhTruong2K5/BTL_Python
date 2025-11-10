from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponse
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: HttpResponse("Chào mừng bạn đến trang chủ!")),
    path('accounts/', include("Apps.Accounts.urls")),
    path('parkings/', include("Apps.Parkings.urls", namespace = 'Parkings')),
    path('billings/', include("Apps.Billings.urls")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
