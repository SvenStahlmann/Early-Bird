from django.urls import path
from . import views

urlpatterns = [
    path('attendance', views.overview, name='attendance_overview'),
    path('rcloot', views.update_loot, name='rc_loot'),
    path('token/add', views.add_token, name='add_token'),
    path('entitlement/add', views.add_entitlement, name='add_entitlement'),
    path('completeAttendance', views.get_complete_attendance, name='complete_attendance'),
]
