from django import template
register = template.Library()


def get_wowhead_item_id(link):
    if len(link.split('/')) >= 4:
        return link.split('/')[3]


register.filter('get_wowhead_item_id', get_wowhead_item_id)
