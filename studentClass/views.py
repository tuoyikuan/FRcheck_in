from django.shortcuts import render
from django.shortcuts import redirect
from db.models import *
# Create your views here.


def allClass(request):
    usr = request.get_signed_cookie("user", default="0", salt="usr")
    s = Student.objects.get(id__username=usr)
    class_lists = StudentMembership.objects.filter(student=s).all()
    tmplist=[]
    for class_list in class_lists:
        tmplist.append({
            'class_id': class_list.class_id.id,
            'class_name': class_list.class_id.class_name,
            'class_info': class_list.class_id.info
        })
    return render(request, "student/studentClass.html", {'class_lists': tmplist})


def addClass(request):
    if request.method == 'POST':
       classId = request.POST.get("classId")
    usr = request.get_signed_cookie("user", default="0", salt="usr")
    s = Student.objects.get(id__username = usr)
    cl = Class.objects.get(id=classId)
    cl.students.add(s)
    return redirect(request, "/studentClass")



