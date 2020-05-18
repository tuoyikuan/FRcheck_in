from django.urls import path, include
from detail.views import *

urlpatterns = [
    path("", detail),
]