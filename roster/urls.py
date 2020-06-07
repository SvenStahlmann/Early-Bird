from django.urls import path
from . import views

urlpatterns = [
    path('overview', views.overview, name='roster_overview'),
    path('character', views.character, name='roster_character'),
    path('search', views.search, name='roster_search'),

    # Ajax
    path('ajax/autocomplete', views.ajax_autocomplete_search, name='roster_autocomplete_search'),
]
