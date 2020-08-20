from django.contrib import admin
from .models import Enchants, RaidDay, Attendance, LootHistory, Entitlement, Softlock


class EnchantsAdmin(admin.ModelAdmin):
    model = Enchants


class RaidDayAdmin(admin.ModelAdmin):
    model = RaidDay


class AttendanceAdmin(admin.ModelAdmin):
    model = Attendance

    search_fields = ('character__name',)

    ordering = ('-raid_day__date',)


class LootHistoryAdmin(admin.ModelAdmin):
    model = LootHistory

    search_fields = ('character__name',)


class EntitlementAdmin(admin.ModelAdmin):
    model = Entitlement


class SoftlockAdmin(admin.ModelAdmin):
    model = Softlock


admin.site.register(Enchants, EnchantsAdmin)
admin.site.register(RaidDay, RaidDayAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(LootHistory, LootHistoryAdmin)
admin.site.register(Entitlement, EntitlementAdmin)
admin.site.register(Softlock, SoftlockAdmin)

