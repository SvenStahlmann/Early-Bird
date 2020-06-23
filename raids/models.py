from django.db import models
from roster.models import Specialization


class Instance(models.Model):
    LOOTSYSTEM_CHOICES = (
        ('SOFTLOCK', 'Softlock'),
        ('LOOTCOUNCIL', 'Loot Council'),
    )

    name = models.CharField(max_length=80, help_text='Name der Instanz.')
    loot_system = models.CharField(max_length=11, choices=LOOTSYSTEM_CHOICES, help_text='Auswahl des Lootsystems.')
    order = models.PositiveIntegerField(blank=False, null=False)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Encounter(models.Model):
    name = models.CharField(max_length=80, unique=True, help_text='Name des Encounteres.')
    order = models.PositiveIntegerField(blank=False, null=False)

    # Foreign Key
    instance = models.ForeignKey(Instance, related_name='encounter', on_delete=models.CASCADE,
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
        ('TOKEN', 'Token'),
        ('MISCELLANEOUS', 'Sonstiges'),
    )

    TYPE_CHOICES = (
        ('CLOTH', 'Stoff'),
        ('LEATHER', 'Leder'),
        ('MAIL', 'Kette'),
        ('PLATE', 'Platte'),
        ('BOW', 'Bogen'),
        ('CROSSBOW', 'Armbrust'),
        ('DAGGER', 'Dolch'),
        ('FISTWEAPON', 'Fauswaffe'),
        ('GUN', 'Schusswaffe'),
        ('AXE', 'Axt'),
        ('MACE', 'Streitkolben'),
        ('SWORD', 'Schwert'),
        ('POLEARM', 'Stangenwaffe'),
        ('STAVE', 'Stab'),
        ('THROWN', 'Wurfwaffe'),
    )

    name = models.CharField(max_length=80, unique=True, help_text='Name des Items.')
    icon = models.ImageField(upload_to='item_icons/', help_text='Icon des Items.')
    quality = models.CharField(max_length=9, choices=QUALITY_CHOICES, help_text='Qualität des Items.')
    slot = models.CharField(max_length=13, choices=SLOT_CHOICES,
                            help_text='Ausrüstungsplatz, an welchem dieses Item angelegt wird.')
    type = models.CharField(max_length=13, choices=TYPE_CHOICES, blank=True, null=True,
                            help_text='Rüstungstyp des Items.')
    wowhead_link = models.URLField(help_text='Hyperlink zum Item auf wowhead.com.')
    order = models.PositiveIntegerField(blank=False, null=False)

    # Many to many
    encounter = models.ManyToManyField(Encounter, related_name='item')

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Token(models.Model):
    # Foreign key
    token_item = models.ForeignKey(Item, related_name='token_item', on_delete=models.CASCADE, help_text='Das entsprechende Token-Item.')

    # Many to Many
    items = models.ManyToManyField(Item, related_name='token_items')

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.token_item)
