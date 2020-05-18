from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from db.models import *


import pdb
# Create your views here.


def register_post(request):
    username = request.POST.get('username')
    password = request.POST.get('password1')
    password_r = request.POST.get('password2')
    email = request.POST.get('email')
    name = request.POST.get('name')
    number = request.POST.get('number')
    dept = request.POST.get('dept')

    if len(User.objects.filter(username=username)) >= 1:
        return render(request, 'registration/sign-up.html', {
            'errors': 'Username has been used.'
        })
    if password != password_r:
        return render(request, 'registration/sign-up.html', {
            'errors': 'Password does not match.',
            'username': username,
            'email': email,
            'name': name,
            'number': number,
            'dept': dept,
        })
    u = User(username=username, email=email, info='', first_name=name,
             last_name='')
    u.set_password(password)
    u.save()

    if int(number) < 10000 & len(Teacher.objects.filter(teacher_id=number)) == 0:
        Teacher.objects.create(id=u, teacher_id=number, dept=dept)
    elif len(Student.objects.filter(student_id=number)) == 0:
        Student.objects.create(id=u, student_id=number, dept=dept)
    # TA.objects.create(id=u, ta_id=number, dept=dept, authority="000")
    return redirect('/accounts/congratulations')


def register(request):
    return render(request, 'registration/sign-up.html')


def congratulations(request):
    return render(request, 'registration/good.html')
