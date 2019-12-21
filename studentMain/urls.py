from django.urls import path
from django.conf.urls import url
from  studentMain.views import *


urlpatterns = [
    url(r'', main),
]