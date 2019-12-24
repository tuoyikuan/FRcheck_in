from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.message_chat, name='message_chat'),
    path('user_main/', views.user_name, name='user_main'),
    path('create_msg/', views.create_msg, name='create_msg'),
    path('delete_msg/<int:e_id>/', views.delete_msg, name='delete_msg'),
    path('chatting/<int:e_id>/', views.chatting, name='chatting'),
    path('chatting/<int:e_id>/create_post/', views.create_post, name='create_post'),
    path('chatting/<int:e_id>/delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
]
