from django.urls import path, include
from studentClass.views import *

urlpatterns = [
    path(r'<int:class_id>/section/', include("section.urls")),
    path(r'<int:class_id>/group/', include("group.urls")),
    path(r'<int:class_id>/discuss/', include("discuss.urls")),
    path(r'<int:class_id>/notification/', include("notification.urls")),
    path(r'<int:class_id>/check/', include("check.urls")),
    path(r'allClass/', allClass, name='all_class'),
    path(r'addClass/', addClass, name='add_class'),
]