from django.urls import path
from . import views

urlpatterns = [
    path('council', views.loot_council, name='loot_council'),
    path('softlock', views.softlock, name='softlock'),
]
