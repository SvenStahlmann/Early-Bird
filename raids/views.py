from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework.utils import json
from earlybirdwebsite.utils import get_instances
from .models import Encounter, Item, Token


def encounter(request):
    if request.method == 'GET':
        if request.GET.get('id'):
            boss_id = request.GET.get('id')
            if Encounter.objects.filter(pk=boss_id).exists():
                # Prepare items
                items = {key[1]: [] for key in Item.SLOT_CHOICES}

                for item in Encounter.objects.get(pk=boss_id).item.all():
                    for tokens in Token.objects.all():
                        if item not in tokens.items.all():
                            items[item.get_slot_display()].append(item)

                # Render page
                return render(request, 'raids/encounter.html',
                              {'instances': get_instances(), 'encounter': Encounter.objects.get(pk=boss_id),
                               'items': items})
        else:
            if Encounter.objects.all().count() > 0:
                # Prepare items
                items = {key[1]: [] for key in Item.SLOT_CHOICES}

                for item in Encounter.objects.order_by('order').first().item.all():
                    for tokens in Token.objects.all():
                        if item not in tokens.items.all():
                            items[item.get_slot_display()].append(item)

                # Render page
                return render(request, 'raids/encounter.html',
                              {'instances': get_instances(), 'encounter': Encounter.objects.order_by('order').first(),
                               'items': items})

    # Return 404 if any of the checks fail
    response = render(request, '404.html')
    response.status_code = 404
    return response


def dispatch_loot_system(request):
    if request.method == 'GET':
        if request.GET.get('loot') and request.GET.get('item'):
            loot = request.GET.get('loot')
            item_id = request.GET.get('item')

            if loot == 'SOFTLOCK':
                return HttpResponseRedirect(reverse('softlock') + '?' + urlencode({'encounter': request.GET.get(
                    'encounter') if request.GET.get('encounter') else -1}) + '&' + urlencode({'item': item_id}))

            if loot == 'LOOTCOUNCIL':
                return HttpResponseRedirect(reverse('loot_council') + '?' + urlencode({'encounter': request.GET.get(
                    'encounter') if request.GET.get('encounter') else -1}) + '&' + urlencode({'item': item_id}))

    # Return 404 if any of the checks fail
    response = render(request, '404.html')
    response.status_code = 404
    return response


def search(request):
    if request.method == 'GET':
        if request.GET.get('search'):
            specifier, pk = request.GET.get('search').split('-')

            if specifier == 'item':
                if Item.objects.filter(pk=pk).exists():
                    return HttpResponseRedirect(reverse('raids_dispatch') + '?' + urlencode(
                        {'loot': Item.objects.get(pk=pk).encounter.first().instance.loot_system, 'item': pk}))

            if specifier == 'encounter':
                if Encounter.objects.filter(pk=pk).exists():
                    return HttpResponseRedirect(reverse('raids_encounter') + '?' + urlencode({'id': pk}))

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
