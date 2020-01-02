from django.urls import path, include
from teacherClass.views import *

urlpatterns = [
    path(r'<int:class_id>/section/', include("section.urls")),
    path(r'<int:class_id>/discuss/', include("discuss.urls")),
    path(r'<int:class_id>/notification/', include("notification.urls")),
    path(r'<int:class_id>/homework/', include("homework.urls")),
    path(r'<int:class_id>/group/', include("group.urls")),
    path(r'allClass/', allClass, name='all_class'),
    path(r'addClass/', addClass, name='add_class'),
    path(r'createClass/', createClass, name='create_class'),
]