from django.urls import path
from . import views

urlpatterns = [
    path('start', views.start_bot, name='start_bot'),

    path('api/add_raid', views.create_raid_day, name='create_raid'),
    path('api/characters', views.get_all_character_names, name='all_character'),
    path('api/entry', views.create_calendar_entry, name='cal_entry'),
    path('api/late_entry', views.create_late_calendar_entry, name='late_entry'),
]
