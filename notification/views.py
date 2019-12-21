from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

from django.db import models
from db.models import *
from django import forms


def show_noti_list(request, class_id):
    temp = Activity.objects.filter(class_id=class_id, type='Notification')
    templist = []
    for e in temp:
        templist.append({
            'noti_id': e.id,
            'title': e.title,
            'content': e.content,
            'create_date': e.create_date,
            'author': e.author.name,
        })

    return render(request, 'notification/notification.html', {
        'note_list': templist,
    })


def show_noti(request, noti_id):
    temp = Activity.objects.get(id=noti_id)
    return render(request, 'notification/show_noti.html', {
        'title': temp.title,
        'content': temp.content,
        'noti': noti_id,
        'isAuthor': True,
    })


def delete_post(request, noti_id):
    temp = Activity.objects.get(id=noti_id)
    class_id = temp.class_id
    temp.delete()
    return redirect('/notification/%d' % class_id.id)


def create_form(request, class_id):
    return render(request, 'notification/new_notification.html', {'class_id': class_id})


def create_post(request, class_id):
    if request.method == 'POST':
        title = request.POST.get('noti-title')
        content = request.POST.get('noti-content')
        Activity.objects.create(
            class_id_id=class_id,
            type='Notification',
            title=title,
            content=content,
            author_id=1,  # TODO
            due_date='2020-12-31',
        )
        return redirect('/notification/%d' % class_id)
    return redirect('/notification/%d' % class_id)

# Create your views here.
