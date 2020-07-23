import datetime

from django import template
register = template.Library()


def get_logged_count(character):
    counter = 0

    for raid_day in character.attendance.all():
        if raid_day.raid_day.date.date() >= datetime.date(2020, 6, 17) and raid_day.present:
            counter += 1

    return counter


register.filter('get_logged_count', get_logged_count)
