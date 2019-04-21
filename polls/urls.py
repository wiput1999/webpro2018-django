from django.urls import path

from polls import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.my_login, name="login"),
    path("logout", views.my_logout, name="logout"),
    path("change_password", views.change_password, name="change_password"),
    path("register", views.register, name="register"),
    path("detail/<int:poll_id>/", views.detail, name="poll_detail"),
    path("detail/<int:poll_id>/create-comment", views.create_comment, name="create_comment"),
    path('detail/<int:question_id>/choice/', views.edit_choice, name='update_choice'),
    path('detail/<int:question_id>/choice/api/', views.edit_choice_api, name='update_choice_api'),
    path("create/", views.create, name='create_poll'),
    path("update/<int:poll_id>/", views.update, name='update_poll'),
    path("delete/<int:question_id>/", views.delete_question, name='delete_question'),
]
