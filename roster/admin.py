from django.contrib import admin
from .models import Profile, WowClass, Specialization, Character


class ProfileAdmin(admin.ModelAdmin):
    model = Profile


class WowClassAdmin(admin.ModelAdmin):
    model = WowClass


class SpecializationAdmin(admin.ModelAdmin):
    model = Specialization


class CharacterAdmin(admin.ModelAdmin):
    model = Character


admin.site.register(Profile, ProfileAdmin)
admin.site.register(WowClass, WowClassAdmin)
admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(Character, CharacterAdmin)


