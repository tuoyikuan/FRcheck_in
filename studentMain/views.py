import os
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from db.models import *
from django.contrib.auth.decorators import login_required



# Create your views here.
import pdb

signal = 0


@login_required
def main(request):
    return render(request,'student/studentMain.html', {'name': request.user.first_name})


@login_required
def upload_ref_photo(request, student_id):
    student = get_object_or_404(Student, id__id=student_id)
    if request.method == "POST":
        file = request.FILES.get("picture")
        if not file:
            return HttpResponse('no file for upload!')
        path = os.path.join("static/file/ref_photos", str(student_id))
        if os.path.exists(path) == False:
            os.makedirs(path)
        destination = open(os.path.join(path, file.name), 'wb')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        url = os.path.join("file/ref_photos", str(student_id), file.name)
        student.ref_photo_url = url
        student.save()
    # todo 根据前端需求决定返回内容
    return




