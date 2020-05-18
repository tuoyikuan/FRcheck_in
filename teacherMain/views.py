from django.shortcuts import render
from django.shortcuts import redirect
from db.models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
import pdb

signal = 0


@login_required
def main(request):
    return render(request, 'teacher/teacherMain.html', {'name': request.user.first_name})



