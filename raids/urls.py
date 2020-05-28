from django.urls import path
from raids import views

urlpatterns = [
    path('page', views.page, name='raid_page')
]
