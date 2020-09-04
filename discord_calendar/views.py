from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

from loot.models import RaidDay
from roster.models import Character
from .models import CalendarEntry, LateSignUp


@csrf_exempt
def create_raid_day(request):

    if request.method == 'GET':
        event_name = request.GET['event']

        # TODO: format date from discord regex
        raid_date = request.GET['date']
        date_time = datetime.strptime(raid_date, '%d-%b-%Y %H:%M')

        raid_day, created = RaidDay.objects.get_or_create(title=event_name, date=date_time)

        if created:
            return HttpResponse("Created")
        else:
            return HttpResponse("Exists")

    else:
        response = render(request, '404.html')
        response.status_code = 404
        return response


@csrf_exempt
def get_all_character_names(request):

    if request.method == 'GET':
        character = Character.objects.all()

        return HttpResponse(serializers.serialize('json', character), content_type='application/json')

    else:
        response = render(request, '404.html')
        response.status_code = 404
        return response


@csrf_exempt
def create_calendar_entry(request):

    if request.method == 'GET':

        character_name = request.GET['character']
        date = datetime.strptime(request.GET['date'], '%d-%b-%Y %H:%M')

        raid_day = RaidDay.objects.get(date=date)
        character = Character.objects.get(name=character_name)

        entry, created = CalendarEntry.objects.get_or_create(character=character, raid_day=raid_day)

        if created:
            return HttpResponse("Created")
        else:
            return HttpResponse("Exists")


@csrf_exempt
def create_late_calendar_entry(request):

    if request.method == 'GET':

        character_name = request.GET['character']
        date = datetime.strptime(request.GET['date'], '%d-%b-%Y %H:%M')

        raid_day = RaidDay.objects.get(date=date)
        character = Character.objects.get(name=character_name)
        entry, created = LateSignUp.objects.get_or_create(character=character, raid_day=raid_day)

        if created:
            return HttpResponse("Created")
        else:
            return HttpResponse("Exists")
