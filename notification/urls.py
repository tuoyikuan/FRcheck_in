from django.urls import path

from .  import views

urlpatterns = [
    # ex: /polls/
    path('<int:class_id>/', views.show_noti_list, name='show_noti_list'),
    path('check/<int:noti_id>/', views.show_noti, name='show_noti'),
    path('create_post/<int:class_id>/', views.create_post, name='create_post'),
    path('delete_post/<int:noti_id>/', views.delete_post, name='delete_post'),
    path('create/<int:class_id>/', views.create_form, name='create_form'),
]
