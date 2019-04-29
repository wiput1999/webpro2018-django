from django.urls import path

from dayoff import views

urlpatterns = [
    path("", views.index, name="dayoff_index"),
]
