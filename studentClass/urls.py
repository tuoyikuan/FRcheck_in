from django.urls import path, include

urlpatterns = [
    path(r'<int:class_id>/section/', include("section.urls")),
    path(r'<int:class_id>/discuss/', include("discuss.urls")),
    path(r'<int:class_id>/notification/', include("notification.urls")),
]