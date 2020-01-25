from django.urls import path
from django.conf.urls import url
from  studentMain.views import *


urlpatterns = [
    path(r'', main, name='sutdent_main'),
    path(r'<int:student_id>/upload', upload_ref_photo) # 注册后，学生上传照片
]