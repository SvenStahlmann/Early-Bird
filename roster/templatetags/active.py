from django import template
register = template.Library()


def active(characters):
    active_characters = []

    for character in characters:
        if character.active:
            active_characters.append(character)

    return active_characters


register.filter('active', active)
