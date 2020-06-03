from django import template
register = template.Library()


def get_attendance(raid_days):
    pass


register.filter('get_attendance', get_attendance)
