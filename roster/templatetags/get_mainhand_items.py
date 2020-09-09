from django import template
from raids.models import Token

register = template.Library()


def get_mainhand_items(character):
    items = []

    for loot in character.loot_history.all():
        if loot.item.slot == 'MAINHAND' or loot.item.slot == 'ONEHAND' or loot.item.slot == 'TWOHAND':
            items.append(loot.item)

    return items


register.filter('get_mainhand_items', get_mainhand_items)
