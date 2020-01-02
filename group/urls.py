from django.urls import path
from django.conf.urls import url
from .views import *


urlpatterns = [
    path(r'', show_group),
    path(r'create/', new_group),
    path(r'create_post/', create_post),
    path(r'join/', join_group),
    path(r'leave/', leave_group),
    path(r'show/<int:gid>/', show_group_members_teacher),
    path(r'lock/<int:gid>/', lock_group),
    path(r'unlock/<int:gid>/', unlock_group),
    path(r'delete/<int:gid>/', delete_group),
    path(r'kick/<int:uid>/', kick_out),
    path(r'lockall/', lock_all),
    path(r'unlockall/', unlock_all),
    path(r'deleteall/', delete_all),
    path(r'nogroup/', no_group),
    path(r'change_ver/', change_ver),
    #path(r'join_post/', join_post),
]
