from django.db.models import Q
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from . import utils
from loot.models import Attendance, RaidDay, LootHistory, Entitlement
from roster.models import Character, Specialization
from raids.models import Item, Instance, Encounter, Token
from io import StringIO
import pandas as pd
import datetime


# Create your views here.
def overview(request):
    if request.user.is_superuser:
        if request.method == 'GET':

            raid_days = RaidDay.objects.all().order_by('-date')
            return render(request, 'attendance/overview.html', {'raidday_exists': True, 'raids': raid_days})

        if request.method == 'POST':
            raid_days = RaidDay.objects.all().order_by('-date')
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
                return render(request, 'attendance/overview.html', {'raidday_exists': False, 'raids': raid_days})

            # iterate over all present players and create an entry in the attendance table
            for player in players:
                try:
                    character = Character.objects.get(name=player.name)
                    all_player = all_player.exclude(name=player.name)

                    # update attendance
                    Attendance.objects.get_or_create(present=True, world_buffs=player.worldbuffs, character=character,
                                                     raid_day=raid)

                    # update enchants
                    for enchant in player.enchants:
                        enchant.update_enchants()

                    player_found.append(player)

                except ObjectDoesNotExist:
                    player_not_found.append(player.name)

            for absent_player in all_player:
                # update attendance
                Attendance.objects.get_or_create(present=False, world_buffs=False, consumables=False,
                                                 character=absent_player, raid_day=raid)

            return render(request, 'attendance/overview.html', {'players': player_found, 'not_found': player_not_found,
                                                                'raidday_exists': True, 'raids': raid_days})

    # Return 404 if any of the checks fail
    response = render(request, '404.html')
    response.status_code = 404
    return response


def update_loot(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            response = redirect('/admin/attendance')
            return response

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
                        LootHistory.objects.get_or_create(character=char, item=item, raid_day=raid_day)

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


def add_token(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            return render(request, 'attendance/token.html', {'instances': Instance.objects.all()})

        if request.method == 'POST':
            if request.POST.get('encounter') and request.POST.get('token') and request.POST.get('items'):
                encounter_id = request.POST.get('encounter')
                token_id = request.POST.get('token')
                item_ids = request.POST.getlist('items')
                token = None
                added = []
                deleted = []

                try:
                    # Check if token has a reference to the encounter
                    if Encounter.objects.get(pk=encounter_id) not in Item.objects.get(pk=token_id).encounter.all():
                        return render(request, 'attendance/token.html', {'instances': Instance.objects.all(),
                                                                         'warning': 'Das Token gehört nicht zum ausgewählten Boss!'})

                    # Check if all items have a reference to the encounter
                    for item in [Item.objects.get(pk=item_id) for item_id in item_ids]:
                        if not any(encounter == Encounter.objects.get(pk=encounter_id) for encounter in item.encounter.all()):
                            return render(request, 'attendance/token.html', {'instances': Instance.objects.all(),
                                                                             'warning': item.name + ' gehört nicht zum ausgewählten Boss!'})

                    # Get or create token
                    (token, created) = Token.objects.get_or_create(token=Item.objects.get(pk=token_id))

                    # If token was created
                    if created:
                        # Set token items of the token
                        token.token_items.set([Item.objects.get(pk=item_id) for item_id in item_ids])
                        new_token = str(token)
                        added.extend([str(Item.objects.get(pk=item_id)) for item_id in item_ids])
                        return render(request, 'attendance/token.html', {'instances': Instance.objects.all(), 'created': new_token, 'added': added})
                    else:
                        items = [Item.objects.get(pk=item_id) for item_id in item_ids]

                        # Get which items were added to the token
                        for item in items:
                            if item not in token.token_items.all():
                                added.append(item)

                        # Get which items were deleted from the token
                        deleted = list(set(list(Token.objects.get(token=Item.objects.get(pk=token_id)).token_items.all())) - set(items))

                        # Update token items of the token
                        token.token_items.set(items)

                        return render(request, 'attendance/token.html', {'instances': Instance.objects.all(), 'added': added, 'deleted': deleted, 'token': token})
                except ObjectDoesNotExist as odne:
                    return render(request, 'attendance/token.html',
                                  {'instances': Instance.objects.all(), 'warning': str(odne), 'added': added, 'deleted': deleted, 'token': token})

    # Return 404 if any of the checks fail
    response = render(request, '404.html')
    response.status_code = 404
    return response


def add_entitlement(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            return render(request, 'attendance/entitlement.html',
                          {'instances': Instance.objects.all(), 'specializations': Specialization.objects.all()})

        if request.method == 'POST':
            if request.POST.get('item') and request.POST.getlist('specializations') and request.POST.getlist(
                    'priority'):
                item_id = request.POST.get('item')
                specialization_ids = request.POST.getlist('specializations')
                priority_ids = request.POST.getlist('priority')
                added = []
                changed = []
                deleted = []

                # Check if a priority has been set for each specialization
                if len(specialization_ids) != len(priority_ids):
                    return render(request, 'attendance/entitlement.html',
                                  {'instances': Instance.objects.all(), 'specializations': Specialization.objects.all(),
                                   'warning': 'Für jede ausgewählte Spezialisierung muss eine Priorität angegeben werden!'})

                # Check for duplicate specializations
                if len(specialization_ids) != len(set(specialization_ids)):
                    return render(request, 'attendance/entitlement.html',
                                  {'instances': Instance.objects.all(), 'specializations': Specialization.objects.all(),
                                   'warning': 'Pro Item darf für jede Spezialisierung nur eine Priorität gesetzt werden!'})

                try:
                    for (specialization, priority) in zip(
                            [Specialization.objects.get(pk=specialization_id) for specialization_id in
                             specialization_ids],
                            priority_ids):
                        (entitlement, created) = Entitlement.objects.get_or_create(item=Item.objects.get(pk=item_id),
                                                                                   specialization=specialization)

                        try:
                            if created:
                                entitlement.priority = int(priority)
                                entitlement.save()
                                added.append(str(entitlement))
                            else:
                                if entitlement.priority != int(priority):
                                    entitlement.priority = int(priority)
                                    entitlement.save()
                                    changed.append(str(entitlement))
                        except ValueError:
                            return render(request, 'attendance/entitlement.html', {'instances': Instance.objects.all(),
                                                                                   'specializations': Specialization.objects.all(),
                                                                                   'warning': 'Prioritäten müssen Zahlen sein! Fehler bei Spezialisierung ' + str(
                                                                                       specialization) + ' und Priorität ' + priority,
                                                                                   'added': added, 'changed': changed})

                    deleted = list(set(list(Entitlement.objects.filter(item=Item.objects.get(pk=item_id)))) - set([Entitlement.objects.get(item=Item.objects.get(pk=item_id), specialization=Specialization.objects.get(pk=specialization_id)) for specialization_id in specialization_ids]))

                    for ent in deleted:
                        ent.delete()

                except ObjectDoesNotExist as odne:
                    return render(request, 'attendance/entitlement.html',
                                  {'instances': Instance.objects.all(), 'specializations': Specialization.objects.all(),
                                   'warning': str(odne), 'added': added, 'changes': changed, 'deleted': deleted})

                return render(request, 'attendance/entitlement.html',
                              {'instances': Instance.objects.all(), 'specializations': Specialization.objects.all(),
                               'added': added, 'changed': changed, 'deleted': [str(ent) for ent in deleted]})

    # Return 404 if any of the checks fail
    response = render(request, '404.html')
    response.status_code = 404
    return response
