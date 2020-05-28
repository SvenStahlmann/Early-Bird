from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import Instance, Encounter, Item


class InstanceAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = Instance


class EncounterAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = Encounter


class ItemAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = Item


admin.site.register(Instance, InstanceAdmin)
admin.site.register(Encounter, EncounterAdmin)
admin.site.register(Item, ItemAdmin)
