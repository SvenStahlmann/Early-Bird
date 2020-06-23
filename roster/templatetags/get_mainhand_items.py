from django import template
from raids.models import Token

register = template.Library()


def get_mainhand_items(character):
    items = []

    for loot in character.loot_history.all():
        if loot.item.slot == 'TOKEN':
            if Token.objects.filter(token=loot.item).exists():
                for token_item in Token.objects.get(token=loot.item).token_items.all():
                    for entitlement in token_item.entitlement.all():
                        if entitlement.specialization == character.specialization:
                            if token_item.slot == 'MAINHAND' or token_item.slot == 'ONEHAND' or token_item.slot == 'TWOHAND':
                                items.append(token_item)
        else:
            if loot.item.slot == 'MAINHAND' or loot.item.slot == 'ONEHAND' or loot.item.slot == 'TWOHAND':
                items.append(loot.item)

    return items


register.filter('get_mainhand_items', get_mainhand_items)
