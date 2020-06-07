from django import template
register = template.Library()


def count_enchants(enchants):
    count = 0

    if enchants.head:
        count += 1

    if enchants.shoulders:
        count += 1

    if enchants.back:
        count += 1

    if enchants.chest:
        count += 1

    if enchants.wrist:
        count += 1

    if enchants.hands:
        count += 1

    if enchants.legs:
        count += 1

    if enchants.legs:
        count += 1

    return count


register.filter('count_enchants', count_enchants)
