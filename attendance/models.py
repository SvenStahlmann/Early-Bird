from django.db import models
from loot.models import Enchants
from roster.models import Character
from enum import Enum


# Create your models here.
class Player(object):

    def __init__(self, name, player_id, worldbuffs, enchants):
        self.name = name
        self.player_id = player_id
        self.worldbuffs = worldbuffs
        self.enchants = enchants

    def __str__(self):
        return str(self.name)


class Enchant(object):

    def __init__(self, slot, enchant, character):

        self.slot = slot
        self.enchant = enchant
        self.character = character

    def update_enchants(self):

        character = Character.objects.get(name=self.character)
        enchants = Enchants.objects.get(character=character)

        # check enchant slot
        if self.slot == Item.HEAD.value:
            enchants.head = self.enchant
        elif self.slot == Item.SHOULDER.value:
            enchants.shoulders = self.enchant
        elif self.slot == Item.CHEST.value:
            enchants.chest = self.enchant
        elif self.slot == Item.LEGS.value:
            enchants.legs = self.enchant
        elif self.slot == Item.BOOTS.value:
            enchants.feet = self.enchant
        elif self.slot == Item.HANDS.value:
            enchants.hands = self.enchant
        elif self.slot == Item.BRACER.value:
            enchants.wrist = self.enchant
        elif self.slot == Item.CLOAK.value:
            enchants.back = self.enchant
        """
        elif self.slot == Item.MAIN:
            enchants.mainhand = self.enchant
        elif self.slot == Item.OFF:
            enchants.offhand = self.enchant
        """
        enchants.save()


class Item(Enum):

    HEAD = 0
    SHOULDER = 2
    CHEST = 4
    LEGS = 6
    BOOTS = 7
    BRACER = 8
    HANDS = 9
    CLOAK = 14
    MAIN = 15
    OFF = 16
    # RANGE = 17
