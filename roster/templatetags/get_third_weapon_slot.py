from django import template
register = template.Library()


def get_third_weapon_slot(character):
    items = []

    for loot in character.loot_history.all():
        if loot.item.slot == 'RELIC' or loot.item.slot == 'RANGED' or loot.item.slot == 'WAND':
            items.append(loot.item)

    return items


register.filter('get_third_weapon_slot', get_third_weapon_slot)