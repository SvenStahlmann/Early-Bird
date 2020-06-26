import requests
import json
from .models import Player, Enchant, Worldbuff
import datetime


# CONSTANT VARIABLES

API_KEY = "15640c4cdecb8dd3d48ebbf7ff485a17"
GUILD_NAME = "Early Bird Express"
SERVER_NAME = "Lucifron"
REGION = "EU"

# URLS
BASE_URL = "https://classic.warcraftlogs.com:443/v1"


def get_attendance_for_raid(raid_name):
    slug = "/reports/guild/{}/{}/{}?api_key={}".format(GUILD_NAME, SERVER_NAME, REGION, API_KEY)
    url = BASE_URL + slug

    req = requests.get(url)
    resp = json.loads(req.content)

    # get last raid
    if raid_name == '':
        report_id = resp[0]['id']
        report_end = resp[0]['end']
    # get specific raid
    else:
        for raid in resp:
            if raid['title'] == raid_name:
                report_id = raid['id']
                report_end = raid['end']
                break

    players = get_present_players(report_id, report_end)
    return players, datetime.datetime.fromtimestamp(report_end//1000)


def get_present_players(report_id, report_end):
    slug = "/report/tables/casts/{}?end={}&api_key={}".format(report_id, report_end, API_KEY)
    url = BASE_URL + slug

    req = requests.get(url)
    resp = json.loads(req.content)

    buffs = []
    for buff in Worldbuff:
        buffs.append(get_worldbuff(report_id, buff.value, report_end))

    players = []
    for x in resp['entries']:
        enchants = []
        worldbuffs = 0
        name = x['name']

        # get player enchants
        for item in x['gear']:
            if 'permanentEnchantName' in item.keys():
                enchants.append(Enchant(item['slot'], True, name))
            else:
                enchants.append(Enchant(item['slot'], False, name))

        # get players worldbuffs
        for buff in buffs:
            for item in buff['auras']:
                if name == item['name']:
                    if item['totalUses'] > 0:
                        worldbuffs += 1
                        break

        players.append(Player(name, worldbuffs, enchants))

    return players


def get_worldbuff(report_id, worldbuff, end):
    slug = "/report/tables/buffs/{}?end={}&abilityid={}&api_key={}".format(report_id, end, worldbuff, API_KEY)
    url = BASE_URL + slug

    req = requests.get(url)
    resp = json.loads(req.content)

    return resp
