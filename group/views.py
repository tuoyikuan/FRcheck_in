from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from db.models import *
from utils.funcs import *

# Create your views here.

signal = 0


def show_student_group(request, class_id):
    usr = request.user.username
    s = Student.objects.get(id__username=usr)
    group = GroupMembership.objects.filter(group__class_id=class_id, student=s).all()
    member_list = []
    is_leader = False
    if len(group):
        group = group[0].group
        member_list = group.members.all()
        is_leader = is_leader_of(request.user.id, group.id)
    length = len(member_list)
    tmplist = []
    for u in member_list:
        tmplist.append({
            'username': u.id.username,
            'is_leader': u == group.leader,
            'group_name': group.name,
            'id': u.id.id,
        })
    global signal
    temp = signal
    signal = 0
    return render(request, "group/group.html", {
        'member_list': tmplist,
        'signal': temp,
        'unlocked': (not group.locked) if len(tmplist) else True,
        'class_id': class_id,
        'is_leader': is_leader,
        'ver_number': (group.ver_number) if len(tmplist) else '',
        'class_name': get_class_name(class_id)
    })


def show_teacher_group(request, class_id):
    user_id = request.user.id
    groups = Group.objects.filter(class_id_id=class_id).all()
    temp_list = []
    for e in groups:
        number = len(GroupMembership.objects.filter(group_id=e.id).all())
        temp_list.append({
            'gid': e.id,
            'name': e.name,
            'number': number,
            'locked': e.locked,
        })
    return render(request, 'group/group_teacher.html', {
        'group_list': temp_list,
        'class_id': class_id,
        'class_name': get_class_name(class_id)
    })


def set_group_lock_by_gid(gid, fl):
    group = Group.objects.get(id=gid)
    group.locked = fl
    group.save()


def delete_group_by_gid(gid):
    group = Group.objects.get(id=gid)
    group.delete()


@login_required
def lock_group(request, class_id, gid):
    if is_teacher_of(request.user.id, class_id):
        set_group_lock_by_gid(gid, True)
        return redirect('/studentClass/%d/group/' % class_id)
    return redirect('/studentClass/denied/')

@login_required
def unlock_group(request, class_id, gid):
    if is_teacher_of(request.user.id, class_id):
        set_group_lock_by_gid(gid, False)
        return redirect('/studentClass/%d/group/' % class_id)
    return redirect('/studentClass/denied/')

@login_required
def delete_group(request, class_id, gid):
    if is_teacher_of(request.user.id, class_id):
        delete_group_by_gid(gid)
        return redirect('/studentClass/%d/group/' % class_id)
    return redirect('/studentClass/denied/')


@login_required
def lock_all(request, class_id):
    if is_teacher_of(request.user.id, class_id):
        groups = Group.objects.filter(class_id_id=class_id).all()
        for e in groups:
            set_group_lock_by_gid(e.id, True)
        return redirect('/studentClass/%d/group/' % class_id)
    return redirect('/studentClass/denied/')


@login_required
def unlock_all(request, class_id):
    if is_teacher_of(request.user.id, class_id):
        groups = Group.objects.filter(class_id_id=class_id).all()
        for e in groups:
            set_group_lock_by_gid(e.id, False)
        return redirect('/studentClass/%d/group/' % class_id)
    return redirect('/studentClass/denied/')


@login_required
def delete_all(request, class_id):
    if is_teacher_of(request.user.id, class_id):
        groups = Group.objects.filter(class_id_id=class_id).all()
        for e in groups:
            delete_group_by_gid(e.id)
        return redirect('/studentClass/%d/group/' % class_id)
    return redirect('/studentClass/denied/')


@login_required
def show_group_members_teacher(request, class_id, gid):
    if is_teacher_of(request.user.id, class_id):
        group = Group.objects.get(id=gid)
        member_list = group.members.all()
        tmplist = []
        for u in member_list:
            tmplist.append({
                'username': u.id.username,
                'is_leader': u == group.leader,
                'group_name': group.name,
            })
        return render(request, "group/group_show_teacher.html", {
            'member_list': tmplist,
            'class_id': class_id,
        })


@login_required
def show_group(request, class_id):
    if is_teacher_of(request.user.id, class_id):
        return show_teacher_group(request, class_id)
    # if is_ta_of(request.user.id, class_id):
    # return show_ta_group(request, class_id)
    if is_student_of(request.user.id, class_id):
        return show_student_group(request, class_id)
    return redirect('/studentClass/denied/')


@login_required
def new_group(request, class_id):
    return render(request, 'group/new_group.html', {
        'class_id': class_id,
    })


@login_required
def create_post(request, class_id):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        ver_number = request.POST.get('ver_number')
        user_id = request.user.id
        if Group.objects.filter(class_id=class_id, ver_number=ver_number).exists():
            return render(request, 'group/new_group.html', {
                'class_id': class_id,
                'signal': 1,
            })
        if GroupMembership.objects.filter(group__class_id_id=class_id, student_id=user_id).exists():
            return render(request, 'group/new_group.html', {
                'class_id': class_id,
                'signal1': 1,
            })
        gr = Group.objects.create(class_id_id=class_id, leader_id=user_id, name=group_name,
                                  ver_number=ver_number, locked=False)
        gr.members.add(Student.objects.get(id_id=user_id))
        gr.save()
    return redirect('/studentClass/%d/group/' % class_id)


@login_required
def change_ver(request, class_id):
    if request.method == 'POST':
        ver_number = request.POST.get('ver_number')
        if Group.objects.filter(class_id=class_id, ver_number=ver_number).exists():
            global signal
            signal=1
            return redirect('/studentClass/%d/group/' % class_id)
        group = Group.objects.get(leader__id_id=request.user.id)
        group.ver_number=ver_number
        group.save()
    return redirect('/studentClass/%d/group/' % class_id)


@login_required
def leave_group(request, class_id):
    if request.method == 'POST':
        u = Student.objects.get(id_id=request.user.id)
        group = GroupMembership.objects.get(group__class_id_id=class_id, student=u).group
        if u == group.leader:
            group.delete()
        else:
            group.members.remove(u)
            group.save()
    return redirect('/studentClass/%d/group/' % class_id)


@login_required
def kick_out(request, class_id, uid):
    if request.method == 'POST':
        if not is_student_of(request.user.id, class_id) and not is_student_of(uid, class_id):
            return redirect('studentClass/denied/')
        u1 = Student.objects.get(id_id=request.user.id)
        u2 = Student.objects.get(id_id=uid)
        group2 = GroupMembership.objects.get(group__class_id_id=class_id, student=u2).group
        if not is_leader_of(u1.id.id, group2.id):
            return redirect('studentClass/denied/')
        group2.members.remove(u2)
        group2.save()
    return redirect('/studentClass/%d/group/' % class_id)


@login_required
def join_group(request, class_id):
    global signal
    if request.method == 'POST':
        ver_number = request.POST.get('ver_number')
        usr = request.user.username
        s = Student.objects.get(id__username=usr)
        try:
            group = Group.objects.get(class_id=class_id, ver_number=ver_number)
        except Exception as e:
            signal = 1
            return redirect("/studentClass/%d/group/" % class_id)
        if group.locked:
            signal = 3
            return redirect("/studentClass/%d/group/" % class_id)
        group.members.add(s)
        group.save()
        signal = 2
    return redirect("/studentClass/%d/group/" % class_id)

@login_required
def no_group(request, class_id):
    if is_teacher_of(request.user.id, class_id):
        students = Class.objects.get(id=class_id).students.all()
        temp_list = []
        for e in students:
            if (not GroupMembership.objects.filter(group__class_id_id=class_id, student=e).exists() and
                not is_teacher_of(e.id.id, class_id)):
                temp_list.append({
                    'username': e.id.username,
                    'is_leader': '未分组',
                })
        return render(request, "group/group_show_teacher.html", {
            'member_list': temp_list,
            'class_id': class_id,
            'no_group': True,
        })
    return redirect('/studentClass/denied/')
