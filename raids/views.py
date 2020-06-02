from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework.utils import json
from earlybirdwebsite.utils import get_instances
from .models import Encounter, Item


def encounter(request):
    if request.method == 'GET':
        if request.GET.get('boss'):
            boss_id = request.GET.get('boss')
            if Encounter.objects.filter(pk=boss_id).exists():
                return render(request, 'raids/encounter.html',
                              {'instances': get_instances(), 'encounter': Encounter.objects.get(pk=boss_id)})

    # Return 404 if any of the checks fail
    response = render(request, '404.html')
    response.status_code = 404
    return response


def dispatch_loot_system(request):
    if request.method == 'GET':
        if request.GET.get('loot') and request.GET.get('item'):
            loot = request.GET.get('loot')
            item = request.GET.get('item')

            if loot == 'SOFTLOCK':
                # TODO: dispatch to softlock view of item
                pass

            if loot == 'LOOTCOUNCIL':
                # TODO: dispatch to loot council view of item
                pass

    # Return 404 if any of the checks fail
    response = render(request, '404.html')
    response.status_code = 404
    return response


def search(request):
    if request.method == 'GET':
        if request.GET.get('search'):
            specifier, pk = request.GET.get('search').split('-')
            encounter_id = False

            if specifier == 'item':
                if Item.objects.filter(pk=pk).exists():
                    # TODO: Show softlock or loot council statistics of item
                    pass

            if specifier == 'encounter':
                if Encounter.objects.filter(pk=pk).exists():
                    encounter_id = Encounter.objects.get(pk=pk).id

            if encounter_id:
                return HttpResponseRedirect(reverse('raids_encounter') + '?' + urlencode({'boss': encounter_id}))

    # Return 404 if any of the checks fail
    response = render(request, '404.html')
    response.status_code = 404
    return response


# Ajax
def ajax_autocomplete_search(request):
    if request.is_ajax():
        # Get search string
        keyword = request.GET.get('search', '').capitalize()

        # Get all encounters and items whose title contains the keyword
        encounters = Encounter.objects.filter(name__contains=keyword)
        items = Item.objects.filter(name__contains=keyword)

        # Prepare names for autocomplete
        names = []

        for encounter in encounters:
            names.append([encounter.name, encounter.id, 'encounter'])

        for item in items:
            names.append([item.name, item.id, 'item'])

        # Encode results list to json data
        data = json.dumps(names)

        # Return HTTPResponse with autocomplete data
        mimetype = 'application/json'

        return HttpResponse(data, mimetype)

    # Return nothing if any of the checks fail
    return JsonResponse({})

def index(request):
    return render(request, 'raids/index.html', {'instances': get_instances()})