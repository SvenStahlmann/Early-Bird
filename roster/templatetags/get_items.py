from django import template
from raids.models import Token

register = template.Library()


def get_items(character, slot):
    items = []

    for loot in character.loot_history.all():
        if loot.item.slot == slot:
            items.append(loot.item)

    return items


register.filter('get_items', get_items)
