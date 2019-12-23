from django.urls import path
from django.conf.urls import url
from  studentMain.views import *


urlpatterns = [
    path(r'', main, name='sutdent_main'),
    path(r'allClass/', allClass, name='all_class'),
    path(r'addClass/', addClass, name='add_class'),
]