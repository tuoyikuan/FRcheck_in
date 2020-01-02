from django.urls import path
from django.conf.urls import url
from  section.views import *

urlpatterns = [
    path('', section),
    path(r'detail/<int:sec_number>/', show_sec),
    path(r'detail/<int:sec_number>/uploadFile/', uploadFile),
    path(r'create/', create),
    path(r'create/new/', create_new_sec),
]