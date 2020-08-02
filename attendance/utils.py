import requests
import json
from .models import Player, Enchant, Worldbuff, Item
from .models import Item as GearItem
from loot.models import RaidDay, LootHistory
from roster.models import Character
from raids.models import Item
from django.core.exceptions import ObjectDoesNotExist
import datetime


# CONSTANT VARIABLES

API_KEY = "15640c4cdecb8dd3d48ebbf7ff485a17"
GUILD_NAME = "Early Bird Express"
SERVER_NAME = "Lucifron"
REGION = "EU"

# URLS
BASE_URL = "https://classic.warcraftlogs.com:443/v1"


def get_attendance_for_raid(raid_date):
    slug = "/reports/guild/{}/{}/{}?api_key={}".format(GUILD_NAME, SERVER_NAME, REGION, API_KEY)
    url = BASE_URL + slug

    req = requests.get(url)
    resp = json.loads(req.content)

    raid_date = datetime.datetime.strptime(raid_date, '%d.%m.%Y')
    raids_on_date = []

    for raid in resp:

        date = datetime.datetime.fromtimestamp(raid['start']//1000)
        date = date.replace(hour=0, minute=0, second=0, microsecond=0)

        if date == raid_date:
            raids_on_date.append(raid)

    first_raid_on_date = raids_on_date[-1]
    report_id = first_raid_on_date['id']
    report_end = first_raid_on_date['end']

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
        for slot in GearItem:
            enchanted = False
            for item in x['gear']:
                if slot.value == item['slot']:
                    if 'permanentEnchantName' in item.keys():
                        enchants.append(Enchant(item['slot'], True, name))
                        enchanted = True
            if not enchanted:
                enchants.append(Enchant(slot.value, False, name))

        # get players worldbuffs
        for buff in buffs:
            for item in buff['auras']:
                if name == item['name']:
                    if item['totalUses'] > 0:
                        worldbuffs += 1
                        break

        # update players gear
        check_items(name, x['gear'])

        players.append(Player(name, worldbuffs, enchants))

    return players


def get_worldbuff(report_id, worldbuff, end):
    slug = "/report/tables/buffs/{}?end={}&abilityid={}&api_key={}".format(report_id, end, worldbuff, API_KEY)
    url = BASE_URL + slug

    req = requests.get(url)
    resp = json.loads(req.content)

    return resp


def check_items(player_name, gear):

    try:
        character = Character.objects.get(name=player_name)
    except ObjectDoesNotExist:
        print("No entry in database for player {}".format(player_name))
        return

    for x in gear:
        try:
            item = Item.objects.get(name=x['name'])
        except ObjectDoesNotExist:
            print("Item {} does not exists".format(x['name']))
            continue
        except KeyError:
            continue
        try:
            LootHistory.objects.get(character=character, item=item)
        except ObjectDoesNotExist:
            print("No loot history entry for item {} and player {}. Entry will be added to LootHistory on default date.".format(x['name'], player_name))

            default_date = datetime.datetime(1900, 1, 1, 9, 0, 0, 0)
            raid_day = RaidDay.objects.get(date=default_date)
            LootHistory.objects.create(character=character, item=item, raid_day=raid_day)



