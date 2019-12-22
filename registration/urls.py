from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('congratulations/', views.congratulations, name='congratulations'),
    path('register_post/', views.register_post, name='register_post'),
]
