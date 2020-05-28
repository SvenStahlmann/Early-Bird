from django.db import models
from roster.models import Specialization


class Instance(models.Model):
    name = models.CharField(max_length=80, help_text='Name der Instanz.')
    order = models.PositiveIntegerField(blank=False, null=False)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Encounter(models.Model):
    name = models.CharField(max_length=80, help_text='Name des Encounteres.')
    order = models.PositiveIntegerField(blank=False, null=False)

    # Foreign Key
    instance = models.ForeignKey(Instance, related_name='Encounter', on_delete=models.CASCADE,
                                 help_text='Instanz, zu welcher dieser Encounter gehört.')

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Item(models.Model):
    QUALITY_CHOICES = (
        ('POOR', 'Schlecht'),
        ('COMMON', 'Gewöhnlich'),
        ('UNCOMMON', 'Außergewöhnlich'),
        ('RARE', 'Selten'),
        ('EPIC', 'Episch'),
        ('LEGENDARY', 'Legendär'),
    )

    SLOT_CHOICES = (
        ('HEAD', 'Kopf'),
        ('NECK', 'Hals'),
        ('SHOULDERS', 'Schultern'),
        ('BACK', 'Rücken'),
        ('CHEST', 'Brust'),
        ('WRIST', 'Handgelenke'),
        ('HANDS', 'Hände'),
        ('WAIST', 'Taille'),
        ('LEGS', 'Beine'),
        ('FEET', 'Füße'),
        ('FINGER', 'Finger'),
        ('TRINKET', 'Schmuck'),
        ('MAINHAND', 'Waffenhand'),
        ('OFFHAND', 'Schildhand'),
        ('ONEHAND', 'Einhändig'),
        ('TWOHAND', 'Zweihändig'),
        ('RANGED', 'Distanz'),
        ('RELIC', 'Relikt'),
    )

    TYPE_CHOICES = (
        ('CLOTH', 'Stoff'),
        ('LEATHER', 'Leder'),
        ('MAIL', 'Kette'),
        ('PLATE', 'Platte')
    )

    name = models.CharField(max_length=80, help_text='Name des Items.')
    icon = models.ImageField(upload_to='item_icons/', help_text='Icon des Items.')
    quality = models.CharField(max_length=9, choices=QUALITY_CHOICES, help_text='Qualität des Items.')
    slot = models.CharField(max_length=9, choices=SLOT_CHOICES,
                            help_text='Ausrüstungsplatz, an welchem dieses Item angelegt wird.')
    type = models.CharField(max_length=7, choices=TYPE_CHOICES, blank=True, null=True,
                            help_text='Rüstungstyp des Items.')
    wowhead_link = models.URLField(help_text='Hyperlink zum Item auf wowhead.com.')
    order = models.PositiveIntegerField(blank=False, null=False)

    # Many to many
    Encounter = models.ManyToManyField(Encounter, related_name='item')

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name
