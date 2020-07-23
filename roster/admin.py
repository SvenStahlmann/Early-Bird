from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import Profile, WowClass, Specialization, Character, Twink


class ProfileAdmin(admin.ModelAdmin):
    model = Profile


class WowClassAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = WowClass


class SpecializationAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = Specialization


class CharacterAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = Character


class TwinkAdmin(admin.ModelAdmin):
    model = Twink


admin.site.register(Profile, ProfileAdmin)
admin.site.register(WowClass, WowClassAdmin)
admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Twink, TwinkAdmin)


