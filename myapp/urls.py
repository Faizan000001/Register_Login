from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    # path('', views.register_page, name='register_page'),
    path('', views.index, name='index'),
    # path('register/', views.index, name='register'),
    # path('login/', views.index, name='register'),
]
