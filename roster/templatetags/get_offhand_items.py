from django import template

from raids.models import Token

register = template.Library()


def get_offhand_items(character):
    items = []

    for loot in character.loot_history.all():
        if loot.item.slot == 'OFFHAND' or loot.item.slot == 'ONEHAND':
            items.append(loot.item)

    return items


register.filter('get_offhand_items', get_offhand_items)
