from django.urls import path, include
from check.views import *

urlpatterns = [
    path("", check),
    path("teacher/<int:check_id>", teacher_check),
    path("student/<int:check_id>", student_check),
]