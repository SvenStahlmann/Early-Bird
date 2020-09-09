
def transform_discord_emoji_to_text(emojis):

    emojis[:] = [x.replace('_', '').replace('empty', ' ') for x in emojis]
    event_name = ''.join(emojis).lower()

    replace_list = [('bwl', 'BWL'), ('aq', 'AQ'), ('mc', 'MC'), ('zg', 'ZG')]
    for item in replace_list:
        event_name = event_name.replace(item[0], item[1])

    return event_name
