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

        return render(request, 'attendance/overview.html')

    if request.method == 'POST':

        player_not_found = []
        player_found = []

        # scrape the data from classic.warcraftlogs
        players, raid_day = utils.get_attendance_for_raid(request.POST['raid'])

        try:
            # get raid day object
            raid_day = RaidDay.objects.get(date__year=raid_day.year,
                                           date__month=raid_day.month,
                                           date__day=raid_day.day)
        except ObjectDoesNotExist:
            return render(request, 'attendance/overview_error.html')

        # iterate over all present players and create an entry in the attendance table
        for player in players:
            try:
                character = Character.objects.get(name=player.name)

                # update attendance
                attendance = Attendance.create(True, player.worldbuffs, character, raid_day, 10)
                attendance.save()

                # update enchants
                for enchant in player.enchants:
                    enchant.update_enchants()

                player_found.append(player)

            except ObjectDoesNotExist:
                player_not_found.append(player.name)

        return render(request, 'attendance/overview.html', {'players': player_found, 'not_found': player_not_found})

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
                date = item['date'].split('/')
                date[2] = '20' + date[2]

                # get character
                try:
                    char = Character.objects.get(name=player)
                    raid_day = RaidDay.objects.get(date__day=date[0],
                                                   date__month=date[1],
                                                   date__year=date[2])
                    item = Item.objects.get(name=item_name)
                    LootHistory.objects.get_or_create(character=char, item=item, raid_day=raid_day, order=1)

                    items_added.append([char, item])

                except ObjectDoesNotExist:
                    faulty_items = True

                print(player + " " + item_name)

        return render(request, 'attendance/overview.html', {'items': items_added, 'faulty': faulty_items})


    # Return 404 if any of the checks fail
    response = render(request, '404.html')
    response.status_code = 404
    return response


