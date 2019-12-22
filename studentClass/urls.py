from django.urls import path
from django.urls import path, include
from django.conf.urls import url
from studentClass.views import *

urlpatterns = [
    path(r'', allClass),
    path(r'addClass/', addClass),
    path(r'section/', include("section.urls")),
    path(r'notification/',include("notification.urls")),
]