from django import template
register = template.Library()


def get_wowhead_item_id(link):
    return link.split('/')[3]


register.filter('get_wowhead_item_id', get_wowhead_item_id)
