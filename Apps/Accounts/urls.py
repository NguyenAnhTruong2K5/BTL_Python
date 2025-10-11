from django.urls import path
from . import views

urlpatterns = [
    # Ví dụ route mặc định
    path("", views.index, name="accounts_index"),
]