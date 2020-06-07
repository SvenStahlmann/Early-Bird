from django import template

register = template.Library()


def get_calendar_entries(character):
    counter = 0

    for raid_day in character.attendance.all():
        if raid_day.calendar_entry:
            counter += 1

    return counter


register.filter('get_calendar_entries', get_calendar_entries)
