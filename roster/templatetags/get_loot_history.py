from django import template

register = template.Library()


def get_loot_history(character):
    # Only filters items for main specialization -> where entitlement is set for the characters specialization
    instances = {}

    for acquisition in character.loot_history.all():
        for entitlement in acquisition.item.entitlement.all():
            if entitlement.specialization == character.specialization:
                if acquisition.item.encounter.all()[0].instance in instances:
                    instances[acquisition.item.encounter.all()[0].instance] += 1
                else:
                    instances[acquisition.item.encounter.all()[0].instance] = 1

    instances_list = []

    for instance, count in instances.items():
        instances_list.append((instance.name, count))

    return instances_list


register.filter('get_loot_history', get_loot_history)
