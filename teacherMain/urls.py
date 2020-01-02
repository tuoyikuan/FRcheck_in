from django.urls import path
from django.conf.urls import url
from  teacherMain.views import *


urlpatterns = [
    path(r'', main, name='teacher_main'),
]