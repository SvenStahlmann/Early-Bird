from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from . import utils
from loot.models import Attendance, RaidDay, LootHistory
from roster.models import Character
from raids.models import Item
from io import StringIO
import pandas as pd
import datetime


# Create your views here.
def overview(request):
    if request.method == 'GET':

        return render(request, 'attendance/overview.html', {'raidday_exists': True})

    if request.method == 'POST':

        all_player = Character.objects.all()
        player_not_found = []
        player_found = []

        # scrape the data from classic.warcraftlogs
        players, raid_day = utils.get_attendance_for_raid(request.POST['raid'])

        try:
            # get raid day object
            raid_day = raid_day.replace(hour=9, minute=0, second=0, microsecond=0)
            raid = RaidDay.objects.get(date=raid_day)
        except ObjectDoesNotExist:
            return render(request, 'attendance/overview.html', {'raidday_exists': False})

        # iterate over all present players and create an entry in the attendance table
        for player in players:
            try:
                character = Character.objects.get(name=player.name)
                all_player = all_player.exclude(name=player.name)

                # update attendance
                Attendance.objects.get_or_create(present=True, world_buffs=player.worldbuffs, character=character,
                                                 raid_day=raid, order=10)

                # update enchants
                for enchant in player.enchants:
                    enchant.update_enchants()

                player_found.append(player)

            except ObjectDoesNotExist:
                player_not_found.append(player.name)

        for absent_player in all_player:
            # update attendance
            Attendance.objects.get_or_create(present=False, world_buffs=False, consumables=False,
                                             character=absent_player, raid_day=raid, order=10)

        return render(request, 'attendance/overview.html', {'players': player_found, 'not_found': player_not_found,
                                                            'raidday_exists': True})

    # Return 404 if any of the checks fail
    response = render(request, '404.html')
    response.status_code = 404
    return response


def update_loot(request):
    if request.method == 'POST':

        # context
        items_added = []
        faulty_items = False

        columns = ['player', 'date', 'time', 'item', 'response']

        data = StringIO(request.POST['loot'])
        df = pd.read_csv(data, sep=',', index_col=False, usecols=columns)

        for idx, item in df.iterrows():

            if item['response'] in ['Offspec/Greed', 'Mainspec/Need', 'Awarded']:

                player = item['player'].split('-')[0]
                item_name = item['item'].replace('[', '').replace(']', '')
                # get datetime
                date = item['date'].split('/')
                date[2] = '20' + date[2]
                dt = datetime.datetime(int(date[2]), int(date[1]), int(date[0]), 9, 0)

                # get character
                try:
                    char = Character.objects.get(name=player)
                    raid_day = RaidDay.objects.get(date=dt)
                    item = Item.objects.get(name=item_name)
                    LootHistory.objects.get_or_create(character=char, item=item, raid_day=raid_day, order=1)

                    items_added.append([char, item])

                except ObjectDoesNotExist:
                    faulty_items = True

                print(player + " " + item_name)

        return render(request, 'attendance/overview.html', {'items': items_added, 'faulty': faulty_items,
                                                            'raidday_exists': True})


    # Return 404 if any of the checks fail
    response = render(request, '404.html')
    response.status_code = 404
    return response


