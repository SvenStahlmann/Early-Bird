from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from raids.models import Instance, Encounter, Item, Token
from roster.models import Specialization


def test(request):
    return render(request, 'raids/base.html')


def index(request):
    return render(request, 'index.html')


def ajax_encounter(request):
    if request.is_ajax():
        if request.GET.get('id'):
            instance_id = request.GET.get('id')
            if Instance.objects.filter(pk=instance_id).exists():
                return HttpResponse(serializers.serialize('json', Instance.objects.get(pk=instance_id).encounter.all()),
                                    content_type='application/json')

    return JsonResponse({})


def ajax_items(request):
    if request.is_ajax():
        if request.GET.get('id'):
            encounter_id = request.GET.get('id')
            if Encounter.objects.filter(pk=encounter_id).exists():
                return HttpResponse(serializers.serialize('json', Encounter.objects.get(pk=encounter_id).item.all()),
                                    content_type='application/json')

    return JsonResponse({})


def ajax_specializations(request):
    if request.is_ajax():
        specializations = []

        for specialization in Specialization.objects.all():
            specializations.append([specialization.id, specialization.wow_class.name, specialization.name])

        return JsonResponse(specializations, safe=False)

    return JsonResponse({})


def ajax_entitlements(request):
    if request.is_ajax():
        if request.GET.get('id'):
            item_id = request.GET.get('id')
            if Item.objects.filter(pk=item_id).exists():
                return JsonResponse([[entitlement.specialization.wow_class.name, entitlement.specialization.name,
                                      entitlement.specialization.id, entitlement.priority] for entitlement in
                                     Item.objects.get(pk=item_id).entitlement.all()], safe=False)

        return JsonResponse({})


def ajax_token_items(request):
    if request.is_ajax():
        if request.GET.get('id'):
            token_id = request.GET.get('id')
            if Item.objects.filter(pk=token_id).exists():
                item = Item.objects.get(pk=token_id)
                split_items = {'selected': {}, 'unselected': {}}
                if Token.objects.filter(token=item).exists():
                    for token_item in Token.objects.get(token=item).token_items.all():
                        if token_item.slot != 'TOKEN':
                            split_items['selected'][token_item.id] = token_item.name

                for encounter in item.encounter.all():
                    for encounter_item in encounter.item.all():
                        if encounter_item.slot != 'TOKEN':
                            split_items['unselected'][encounter_item.id] = encounter_item.name

                return JsonResponse(split_items)

    return JsonResponse({})

