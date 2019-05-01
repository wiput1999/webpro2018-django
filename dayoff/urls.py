from django.urls import path

from dayoff import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.my_login, name='login'),
    path('create/', views.create, name='create-dayoff'),
]
