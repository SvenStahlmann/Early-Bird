from django.contrib import admin
from .models import CalendarEntry, LateSignUp


# Register your models here.
class CalendarAdmin(admin.ModelAdmin):
    model = CalendarEntry

    search_fields = ('character__name',)


class LateSignUpAdmin(admin.ModelAdmin):
    model = LateSignUp

    search_fields = ('character__name',)


admin.site.register(CalendarEntry, CalendarAdmin)
admin.site.register(LateSignUp, LateSignUpAdmin)
