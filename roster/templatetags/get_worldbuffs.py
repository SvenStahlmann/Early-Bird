from django import template
register = template.Library()


def get_world_buffs(character):
    counter = 0

    for raid_day in character.attendance.all():
        if raid_day.world_buffs:
            counter += 1

    return counter


register.filter('get_world_buffs', get_world_buffs)
