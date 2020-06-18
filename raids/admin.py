from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import Instance, Encounter, Item, Token


class InstanceAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = Instance


class EncounterAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = Encounter
    list_display = ['name', 'instance']


class ItemAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = Item


class TokenAdmin(admin.ModelAdmin):
    model = Token


admin.site.register(Instance, InstanceAdmin)
admin.site.register(Encounter, EncounterAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Token, TokenAdmin)
