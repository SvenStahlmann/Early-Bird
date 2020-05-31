from django.db import models
from roster.models import Character, Specialization
from raids.models import Instance, Item


class Enchants(models.Model):
    head = models.BooleanField(help_text='Verzauberung am Ausrüstungsplatz Kopf.')
    shoulders = models.BooleanField(help_text='Verzauberung am Ausrüstungsplatz Schultern.')
    back = models.BooleanField(help_text='Verzauberung am Ausrüstungsplatz Rücken.')
    chest = models.BooleanField(help_text='Verzauberung am Ausrüstungsplatz Brust.')
    wrist = models.BooleanField(help_text='Verzauberung am Ausrüstungplatz Handgelenk.')
    hands = models.BooleanField(help_text='Verzauberung am Ausrüstungsplatz Hände.')
    legs = models.BooleanField(help_text='Verzauberung am Ausrüstungsplatz Beine.')
    feet = models.BooleanField(help_text='Verzauberung am Ausrüstungsplatz Füße.')
    order = models.PositiveIntegerField(blank=False, null=False)

    # One to one
    character = models.OneToOneField(Character, related_name='enchants', on_delete=models.CASCADE)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return str(self.character)


class RaidDay(models.Model):
    date = models.DateTimeField(help_text='Datum des Raids.')
    order = models.PositiveIntegerField(blank=False, null=False)

    # Foreign key
    instance = models.ForeignKey(Instance, related_name='raid_day', on_delete=models.CASCADE)

    # Many to many
    character = models.ManyToManyField(Character, through='Attendance')

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return str(self.instance) + ' - ' + str(self.date)


class Attendance(models.Model):
    present = models.BooleanField(help_text='Anwesenheit des Charakters am Raidtag.')
    calendar_entry = models.BooleanField(default=True, help_text='Ist der Charakter im Kalender eingetragen.')
    world_buffs = models.BooleanField(default=True, help_text='Hatte der Charakter mindestens 2 von 5 World Buffs am Raidtag.')
    consumables = models.BooleanField(default=True, help_text='Hat der Charakter am Raidtag ausreichend Consumables eingeworfen.')
    misconduct = models.BooleanField(help_text='Jegliches Fehlverhalten des Charakters, z.B. zu spät zum Raid erschienen.')
    comment = models.TextField(blank=True, null=True, help_text='Kommentar zum Charakter am Raidtag.')
    order = models.PositiveIntegerField(blank=False, null=False)

    # Foreign keys
    character = models.ForeignKey(Character, related_name='attendance', on_delete=models.CASCADE)
    raid_day = models.ForeignKey(RaidDay, related_name='attendance', on_delete=models.CASCADE)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return str(self.raid_day) + ' - ' + str(self.character)


class LootHistory(models.Model):
    # Foreign Keys
    character = models.ForeignKey(Character, related_name='loot_history', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='loost_history', on_delete=models.CASCADE)
    raid_day = models.ForeignKey(RaidDay, related_name='loost_history', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(blank=False, null=False)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return str(self.character) + ' - ' + str(self.item) + ' - ' + str(self.raid_day)


class Entitlement(models.Model):
    priority = models.PositiveIntegerField()
    order = models.PositiveIntegerField(blank=False, null=False)

    # Foreign Keys
    item = models.ForeignKey(Item, related_name='entitlement', on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization, related_name='entitlement', on_delete=models.CASCADE)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return str(self.item) + ' - ' + str(self.specialization) + ' - ' + str(self.priority)


class Softlock(models.Model):
    priority = models.IntegerField(blank=True, null=True, help_text='Priorität für Hardlocks.')

    # Foreign keys
    item = models.ForeignKey(Item, related_name='softlock', on_delete=models.CASCADE)
    character = models.OneToOneField(Character, related_name='softlock', on_delete=models.CASCADE)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.character) + ' - ' + str(self.item)