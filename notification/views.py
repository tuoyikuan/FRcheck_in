from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.db import models
from db.models import *
from utils.funcs import *
from django import forms


import pdb
@login_required
def show_noti_list(request, class_id):

    # todo 在teacerClass中加入denied相应的url和view
    # if not in_class(request.user.id, class_id):
    #     return redirect('/teacherClass/denied')

    temp = Activity.objects.filter(class_id=class_id, type='Notification')
    templist = []
    for e in temp:
        templist.append({
            'noti_id': e.id,
            'title': e.title,
            'content': e.content,
            'create_date': e.create_date,
            'author': e.author.username,
            'class_id': class_id,
        })

    return render(request, 'notification/notification.html', {
        'note_list': templist,
        'class_id': class_id,
        'isteacher': is_teacher_of(request.user.id, class_id),
    })


@login_required
def show_noti(request, class_id, noti_id):
    temp = Activity.objects.get(id=noti_id)
    class_id1 = temp.class_id

    temp = Activity.objects.get(id=noti_id)
    return render(request, 'notification/show_noti.html', {
        'title': temp.title,
        'content': temp.content,
        'noti': noti_id,
        'isAuthor': temp.author.id == request.user.id,
        'class_id': class_id,
    })


@login_required
def delete_post(request, class_id, noti_id):
    temp = Activity.objects.get(id=noti_id)
    class_id1 = temp.class_id
    #if not in_class(request.user.id, class_id1.id):
        #return redirect('/teacherClass/denied')
    #temp.delete()
    return redirect('/teacherClass/%d/notification/' % class_id1.id)


@login_required
def create_form(request, class_id):
    #if not in_class(request.user.id, class_id):
        #return redirect('/teacherClass/denied')
    return render(request, 'notification/new_notification.html', {'class_id': class_id})


@login_required
def create_post(request, class_id):
    #if not in_class(request.user.id, class_id):
        #return redirect('/teacherClass/denied')
    if request.method == 'POST':
        title = request.POST.get('noti-title')
        content = request.POST.get('noti-content')
        Activity.objects.create(
            class_id_id=class_id,
            type='Notification',
            title=title,
            content=content,
            author_id=request.user.id,
            due_date='2099-12-31',
        )
        return redirect('/teacherClass/%d/notification/' % class_id)
    return redirect('/teacherClass/%d/notification/' % class_id)

# Create your views here.
