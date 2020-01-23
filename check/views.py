from django.http import HttpResponse
from django.shortcuts import render, redirect
from db.models import *
from django.contrib.auth.decorators import login_required
from django.utils import  timezone
from utils.funcs import *
from django.contrib import messages
import os


@login_required
def check(request, class_id):

    return

@login_required
def teacher_check(request, class_id, check_id):
    return

@login_required
def student_check(request, class_id, check_id):
    return

@login_required
def create(request, class_id):
    checks = Check.objects.filter().all()
    check_id_new = checks[-1].numberz + 1
    cl = Class.objects.get(id=class_id)
    check = Check(class_id=cl, number=check_id_new, check_string="0")
    check.save()
    return redirect("/teacherClass/%d/check" %class_id)