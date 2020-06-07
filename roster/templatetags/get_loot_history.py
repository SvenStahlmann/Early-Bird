from django import template
from raids.utils import get_instances

register = template.Library()


def get_loot_history(character):
    # Only filters items for main specialization -> where entitlement is set for the characters specialization
    # Dict for easy checking if instance is already a key
    instances = {instance: 0 for instance in get_instances()}

    for acquisition in character.loot_history.all():
        for entitlement in acquisition.item.entitlement.all():
            if entitlement.specialization == character.specialization:
                if acquisition.item.encounter.all()[0].instance in instances:
                    instances[acquisition.item.encounter.all()[0].instance] += 1

    # Need to return the loot history as list of sets
    return [(instance, count) for instance, count in instances.items()]


register.filter('get_loot_history', get_loot_history)
