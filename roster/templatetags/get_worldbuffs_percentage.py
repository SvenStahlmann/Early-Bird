import datetime
from .get_worldbuffs import get_world_buffs

from django import template
register = template.Library()


def get_worldbuffs_percentage(character):
    wbfs = get_world_buffs(character)
    attendance = 0

    for raid_day in character.attendance.all():
        if raid_day.raid_day.date.date() >= datetime.date(2020, 6, 17) and raid_day.present:
            attendance += 1

    return wbfs/attendance*100


register.filter('get_worldbuffs_percentage', get_worldbuffs_percentage)
