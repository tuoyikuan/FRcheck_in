from django.urls import path, include
from check.views import *

urlpatterns = [
    path("", check),
    path("create/", create),
    path("create/new", create_new),
    path("teacher/<int:check_id>", teacher_check),
    path("teacher/<int:check_id>/update", update_check),
]