from django import template

register = template.Library()


def strip_time(date):
    return date.strftime("%d.%M.%Y")


register.filter('strip_time', strip_time)
