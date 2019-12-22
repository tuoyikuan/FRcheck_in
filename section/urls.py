from django.urls import path
from django.conf.urls import url
from  section.views import *

urlpatterns = [
    path(r'', section),
]