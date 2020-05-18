from django.shortcuts import render
from db.models import *
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from utils.funcs import *

@login_required
def detail(request, class_id):
    return