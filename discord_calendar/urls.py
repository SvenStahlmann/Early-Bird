from django.urls import path
from . import views

urlpatterns = [
    path('start', views.start_bot, name='start_bot'),
]
