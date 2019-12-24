from django.urls import path
from django.conf.urls import url
from  section.views import *

urlpatterns = [
    path('', section),
    path('detail/<int:sec_number>/', show_sec),
    path('create/', create),
    path('create/new/', create_new_sec),
]