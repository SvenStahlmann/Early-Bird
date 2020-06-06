from django import template
register = template.Library()


def get_consumables(character):
    counter = 0

    for raid_day in character.attendance.all():
        if raid_day.consumables:
            counter += 1

    return counter


register.filter('get_consumables', get_consumables)
