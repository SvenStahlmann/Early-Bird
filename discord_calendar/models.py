from django.db import models
from django.utils import timezone
from roster.models import Character
from loot.models import RaidDay


# Create your models here.
class CalendarEntry(models.Model):

    character = models.ForeignKey(Character, related_name='calendar_entry', on_delete=models.CASCADE)
    raid_day = models.ForeignKey(RaidDay, related_name='raid_day', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['raid_day__date']

    def __str__(self):
        return str(self.raid_day) + ' - ' + str(self.character)


class LateSignUp(models.Model):

    character = models.ForeignKey(Character, related_name='late_sign_up_entry', on_delete=models.CASCADE)
    raid_day = models.ForeignKey(RaidDay, related_name='late_sign_up_day', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['raid_day__date']

    def __str__(self):
        return str(self.raid_day) + ' - ' + str(self.character)
