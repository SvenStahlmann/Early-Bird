from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import Enchants, RaidDay, Attendance, LootHistory, Entitlement, Softlock


class EnchantsAdmin(admin.ModelAdmin):
    model = Enchants


class RaidDayAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = RaidDay


class AttendanceAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = Attendance


class LootHistoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = LootHistory


class EntitlementAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = Entitlement


class SoftlockAdmin(admin.ModelAdmin):
    model = Softlock


admin.site.register(Enchants, EnchantsAdmin)
admin.site.register(RaidDay, RaidDayAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(LootHistory, LootHistoryAdmin)
admin.site.register(Entitlement, EntitlementAdmin)
admin.site.register(Softlock, SoftlockAdmin)

