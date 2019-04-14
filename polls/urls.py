from django.urls import path

from polls import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.my_login, name="login"),
    path("logout", views.my_logout, name="logout"),
    path("detail/<int:poll_id>/", views.detail, name="poll_detail"),
    path("create/", views.create, name='create_poll')
]
