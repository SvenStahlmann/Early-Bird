from django import template

from raids.models import Token

register = template.Library()


def get_third_weapon_slot(character):
    items = []

    for loot in character.loot_history.all():
        if loot.item.slot == 'TOKEN':
            if Token.objects.filter(token_item=loot.item).exists():
                for token_item in Token.objects.get(token_item=loot.item).items.all():
                    for entitlement in token_item.entitlement.all():
                        if entitlement.specialization == character.specialization:
                            if token_item.slot == 'RELIC' or token_item.slot == 'RANGED' or token_item.slot == 'WAND':
                                items.append(token_item)
        else:
            if loot.item.slot == 'RELIC' or loot.item.slot == 'RANGED' or loot.item.slot == 'WAND':
                items.append(loot.item)

    return items


register.filter('get_third_weapon_slot', get_third_weapon_slot)