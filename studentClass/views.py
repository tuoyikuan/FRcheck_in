# noting to do here, only redirect in urls.py
from django.shortcuts import render
from django.shortcuts import redirect
from db.models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
import pdb

signal = 0

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
            'class_info': (cl.class_id.info if len(cl.class_id.info) else "暂无简介")[:100]
        })
    global signal
    temp = signal
    signal = 0
    return render(request, "student/studentClass.html", {
        'class_list': tmplist,
        'username': usr,
        'len': length,
        'signal': temp,
    })


@login_required
def addClass(request):
    global signal
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        usr = request.user.username
        s = Student.objects.get(id__username=usr)
        try:
            cl = Class.objects.filter(id=class_id).all()
        except Exception as e:
            signal = 1
            return redirect("/studentClass")
        if len(cl) != 0:
            studentsInThisClass = StudentMembership.objects.filter(class_id=cl[0]).all()
            if len(studentsInThisClass) == 0:
                class_rank = 1
            else:
                class_rank = studentsInThisClass.latest().class_rank + 1
            new_relation = StudentMembership(class_id=cl[0], student=s, class_rank=class_rank)
            new_relation.save()
            signal = 2
        else:
            signal = 1
    return redirect("/studentClass/allClass")
