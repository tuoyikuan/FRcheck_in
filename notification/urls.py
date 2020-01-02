from django.urls import path
from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.show_noti_list, name='show_noti_list'),
    path('check/<int:noti_id>/', views.show_noti, name='show_noti'),
    path('create_post/', views.create_post, name='create_post'),
    path('delete_post/<int:noti_id>/', views.delete_post, name='delete_post'),
    path('create/', views.create_form, name='create_form'),
]
