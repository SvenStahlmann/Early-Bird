from django import template
register = template.Library()


def get_attendance(character):
    counter = 0

    for raid_day in character.attendance.all():
        if raid_day.present:
            counter += 1

    return counter


register.filter('get_attendance', get_attendance)
