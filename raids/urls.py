from django.urls import path
from raids import views

urlpatterns = [
    path('encounter', views.encounter, name='raids_encounter'),
    path('dispatch', views.dispatch_loot_system, name='raids_dispatch'),

    # Ajax
    path('ajax/autocomplete', views.ajax_autocomplete_search, name='raids_autocomplete_search'),
]
