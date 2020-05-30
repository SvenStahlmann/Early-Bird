from django.shortcuts import render
from earlybirdwebsite.utils import get_instances
from .models import Encounter


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
                pass

            if loot == 'LOOTCOUNCIL':
                pass

    # Return 404 if any of the checks fail
    response = render(request, '404.html')
    response.status_code = 404
    return response
