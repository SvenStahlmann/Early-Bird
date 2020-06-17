from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.http import urlencode
from django.core.exceptions import ObjectDoesNotExist
from . import utils
from loot.models import Attendance, RaidDay
from roster.models import Character


# Create your views here.
def overview(request):
    if request.method == 'GET':

        player_not_found = []

        # scrape the data from classic.warcraftlogs
        players, raid_day = utils.get_attendance_for_last_raid()

        # create a new raid day
        raid_day = RaidDay.create(raid_day, 10)
        raid_day.save()

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

            except ObjectDoesNotExist:
                player_not_found.append(player.name)

    # Return 404 if any of the checks fail
    response = render(request, '404.html')
    response.status_code = 404
    return response
