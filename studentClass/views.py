from django.shortcuts import render
from django.shortcuts import redirect
from db.models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# Create your views here.

@login_required
def allClass(request):
    usr = request.user.username
    s = Student.objects.filter(id__username=usr)
    if len(s):
        class_list = StudentMembership.objects.filter(student=s[0])
    else:
        class_list = []
    tmplist = []
    for cl in class_list:
        tmplist.append({
            'class_id': cl.class_id.id,
            'class_name': cl.class_id.class_name,
            'class_info': cl.class_id.info
        })
    return render(request, "student/studentClass.html", {'class_list': tmplist})


def addClass(request):
    if request.method == 'POST':
        class_id = request.POST.get("classId")
    usr = request.get_signed_cookie("user", default="0", salt="usr")
    s = Student.objects.filter(id__username=usr)[0]
    cl = Class.objects.get(id=class_id)
    cl.students.add(s)
    return redirect(request, "/studentClass")
