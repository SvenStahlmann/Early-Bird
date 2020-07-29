from django.urls import path
from . import views

urlpatterns = [
    path('attendance', views.overview, name='attendance_overview'),
    path('rcloot', views.update_loot, name='rc_loot'),
    path('token', views.add_token, name='add_token'),
    path('entitlement', views.add_entitlement, name='add_entitlement'),
    path('attendance/update', views.update_attendance, name='update_attendance'),
]
