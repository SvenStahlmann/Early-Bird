from django.contrib import admin
from .models import Instance, Boss, Item


class InstanceAdmin(admin.ModelAdmin):
    model = Instance


class BossAdmin(admin.ModelAdmin):
    model = Boss


class ItemAdmin(admin.ModelAdmin):
    model = Item


admin.site.register(Instance, InstanceAdmin)
admin.site.register(Boss, BossAdmin)
admin.site.register(Item, ItemAdmin)
