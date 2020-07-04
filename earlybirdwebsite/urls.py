"""earlybirdwebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('ebeadmin/', admin.site.urls),
    path('loot/', include('loot.urls')),
    path('raids/', include('raids.urls')),
    path('roster/', include('roster.urls')),
    path('admin/', include('attendance.urls')),

    path('test', views.test, name='test'),
    path('', views.index, name='index'),

    # Ajax
    path('ajax/encounter', views.ajax_encounter, name='ajax_encounter'),
    path('ajax/items', views.ajax_items, name='ajax_items'),
    path('ajax/specializations', views.ajax_specializations, name='ajax_specializations'),
    path('ajax/entitlements', views.ajax_entitlements, name='ajax_entitlements'),
    path('ajax/token_items', views.ajax_token_items, name='ajax_token_items'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
