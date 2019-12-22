from django.shortcuts import render
from django.shortcuts import redirect
from db.models import *
from django.db.models import Q


# Create your views here.


def allClass(request):
    usr = request.get_signed_cookie("user", default="0", salt="usr")
    s = Student.objects.filter(id__username=usr)
    if len(s):
        class_lists = StudentMembership.objects.filter(student=s).all()
    else:
        class_lists = []
    tmplist = []
    for class_list in class_lists:
        tmplist.append({
            'class_id': class_list.class_id.id,
            'class_name': class_list.class_id.class_name,
            'class_info': class_list.class_id.info
        })
    return render(request, "student/studentClass.html", {'class_lists': tmplist})


def addClass(request):
    if request.method == 'POST':
        class_id = request.POST.get("classId")
    pdb.set_trace()
    usr = request.get_signed_cookie("user", default="0", salt="usr")
    s = Student.objects.filter(id__username=usr)[0]
    cl = Class.objects.get(id=class_id)
    cl.students.add(s)
    return redirect(request, "/studentClass")
