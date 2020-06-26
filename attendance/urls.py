from django.urls import path
from . import views

urlpatterns = [
    path('attendance', views.overview, name='attendance_overview'),
    path('rcloot', views.update_loot, name='rc_loot'),
]
