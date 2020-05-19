from django.shortcuts import render
from db.models import *
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from utils.funcs import *

@login_required
def detail(request, class_id):
    cl = Class.objects.get(id=class_id)
    class_name = cl.class_name
    students = StudentMembership.objects.filter(class_id=cl).all()
    tempList = []
    for student in students:
        tempList.append({
            "name": student.id.usrname,
            "id": student.student_id,
            "url": student.ref_photo_url
        })
    length = len(tempList)
    return render(request, "detail/detail.html", {
        "class_id": class_id,
        "student_lists": tempList,
        "class_name": class_name,
        "len": length
    })
