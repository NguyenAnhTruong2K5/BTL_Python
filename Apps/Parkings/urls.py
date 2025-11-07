from django.urls import path
from Apps.Parkings import views

app_name = 'Parkings'

urlpatterns = [
    path("", views.index, name="parking_index"),
    path("check-in/", views.check_in, name="check_in"),
    path("check-out/", views.check_out, name="check_out"),
    path("check-out/manual/<int:record_id>/", views.manual_authentication, name="manual_authentication"),
    path("lost-card/", views.lost_card, name="lost_card"),
    path("history/", views.parking_history, name="parking_history"),
    path("add-card/", views.add_card, name="add_card"),
]