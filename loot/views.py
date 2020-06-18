from django.shortcuts import render
from raids.utils import get_instances
from raids.models import Encounter, Item
from loot.models import LootHistory, Softlock


def loot_council(request):
    if request.method == 'GET':
        if request.GET.get('item') and request.GET.get('encounter'):
            item_id = request.GET.get('item')
            encounter_id = request.GET.get('encounter')
            if Item.objects.filter(pk=item_id).exists():
                item = Item.objects.get(pk=item_id)

                if Encounter.objects.filter(pk=encounter_id).exists():
                    encounter = Encounter.objects.get(pk=encounter_id)
                else:
                    encounter = item.encounter.first()

                characters = {}

                # Iterate through all entitlements
                for entitled in item.entitlement.all():
                    # Iterate over all characters of the specialization that is specified in the current entitlement
                    for character in entitled.specialization.character.all():
                        # If character is active
                        if character.active:
                            # If the character has not yet received the item
                            if not LootHistory.objects.filter(character=character, item=item):
                                if entitled.priority in characters:
                                    characters[entitled.priority].append(character)
                                else:
                                    characters[entitled.priority] = [character]

                return render(request, 'loot/loot_council.html', {'instances': get_instances(), 'encounter': encounter,
                                                                  'characters': sorted(characters.items())})

    # Return 404 if any of the checks fail
    response = render(request, '404.html')
    response.status_code = 404
    return response


def softlock(request):
    if request.method == 'GET':
        if request.GET.get('encounter') and request.GET.get('item'):
            item_id = request.GET.get('item')
            encounter_id = request.GET.get('encounter')
            if Item.objects.filter(pk=item_id).exists():
                item = Item.objects.get(pk=item_id)

                if Encounter.objects.filter(pk=encounter_id).exists():
                    encounter = Encounter.objects.get(pk=encounter_id)
                else:
                    encounter = item.encounter.first()

                characters = {}

                # Iterate through all softlocks specified for this item
                for lock in Softlock.objects.filter(item=item):
                    # If character is active
                    if lock.character.active:
                        if not LootHistory.objects.filter(character=lock.character, item=item):
                            if lock.priority in characters:
                                characters[lock.priority].append(lock.character)
                            else:
                                characters[lock.priority] = [lock.character]

                return render(request, 'loot/softlock.html', {'instances': get_instances(), 'encounter': encounter, 'item': item,
                                                              'characters': sorted(characters.items())})

    # Return 404 if any of the checks fail
    response = render(request, '404.html')
    response.status_code = 404
    return response
