from django import template
register = template.Library()


def get_misconduct(character):
    counter = 0

    for raid_day in character.attendance.all():
        if raid_day.misconduct:
            counter += 1

    return counter


register.filter('get_misconduct', get_misconduct)
