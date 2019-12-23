from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.message_chat, name='message_chat'),
    path('user_main/', views.user_name, name='user_main'),
    path('create_msg/', views.create_msg, name='create_msg'),
    path('delete_msg/<int:e_id>/', views.delete_msg, name='delete_msg'),
    path('chatting/<int:e_id>/', views.chatting, name='chatting'),
]
