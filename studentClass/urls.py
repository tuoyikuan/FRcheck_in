from django.urls import path
from django.urls import path
from django.conf.urls import url
from studentClass.views import *

urlpatterns = [
    url(r'', allClass),
    url(r'addClass', addClass),
]