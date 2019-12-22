from django.shortcuts import render
from django.shortcuts import redirect
from db.models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# Create your views here.
import pdb
@login_required
def allClass(request):
    usr = request.user.username
    s = Student.objects.get(id__username=usr)
    class_list = StudentMembership.objects.filter(student=s)
    length = len(class_list)
    tmplist = []
    for cl in class_list:
        tmplist.append({
            'class_id': cl.class_id.id,
            'class_name': cl.class_id.class_name,
            'class_info': cl.class_id.info[:100]
        })
    return render(request, "student/studentClass.html", {'class_list': tmplist, 'username': usr, 'len': length})


def addClass(request):
    pdb.set_trace()
    if request.method == 'POST':
        class_id = request.POST.get("classId")
        usr = request.user.username
        s = Student.objects.get(id__username=usr)
        cl = Class.objects.get(id=class_id)
        cl.students.add(s)
        cl.save()
    return redirect("/studentClass")
