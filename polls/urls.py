from django.urls import path

from polls import views

urlpatterns = [
    path("", views.index, name="index"),
    path("detail/<int:poll_id>/", views.detail, name="poll_detail"),
    path("create/", views.create, name='create_poll')
]
