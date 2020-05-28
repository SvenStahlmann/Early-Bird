from django.contrib import admin
from .models import Enchants, RaidDay, Attendance, LootHistory, Entitlement


class EnchantsAdmin(admin.ModelAdmin):
    model = Enchants


class RaidDayAdmin(admin.ModelAdmin):
    model = RaidDay


class AttendanceAdmin(admin.ModelAdmin):
    model = Attendance


class LootHistoryAdmin(admin.ModelAdmin):
    model = LootHistory


class EntitlementAdmin(admin.ModelAdmin):
    model = Entitlement


admin.site.register(Enchants, EnchantsAdmin)
admin.site.register(RaidDay, RaidDayAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(LootHistory, LootHistoryAdmin)
admin.site.register(Entitlement, EntitlementAdmin)

