from django.shortcuts import redirect
from utils.funcs import *

def home_page(request):
    if len(Teacher.objects.filter(id=request.user.id)) > 0:
        return redirect('/teacherMain')
    else:
        return redirect('/studentMain')