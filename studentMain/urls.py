from django.urls import path
from django.conf.urls import url
from  studentMain.views import *


urlpatterns = [
    path(r'', main, name='sutdent_main'),
]