from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework.utils import json
from .utils import get_classes
from .models import Specialization, Character


def overview(request):
    if request.method == 'GET':
        if request.GET.get('id'):
            specialization_id = request.GET.get('id')
            if Specialization.objects.filter(pk=specialization_id).exists():
                return render(request, 'roster/overview.html', {'classes': get_classes(),
                                                                'specialization': Specialization.objects.get(
                                                                    pk=specialization_id)})
        else:
            if Specialization.objects.all().count() > 0:
                return render(request, 'roster/overview.html', {'classes': get_classes(),
                                                                'specialization': Specialization.objects.order_by(
                                                                    'order').first()})

    # Return 404 if any of the checks fail
    response = render(request, '404.html')
    response.status_code = 404
    return response


def character(request):
    if request.method == 'GET':
        if request.GET.get('id'):
            character_id = request.GET.get('id')
            if Character.objects.filter(pk=character_id).exists():
                return render(request, 'roster/character.html',
                              {'classes': get_classes(), 'character': Character.objects.get(pk=character_id)})

    # Return 404 if any of the checks fail
    response = render(request, '404.html')
    response.status_code = 404
    return response


def search(request):
    if request.method == 'GET':
        if request.GET.get('search'):
            specifier, pk = request.GET.get('search').split('-')

            if specifier == 'specialization':
                if Specialization.objects.filter(pk=pk).exists():
                    return HttpResponseRedirect(reverse('roster_overview') + '?' + urlencode({'id': pk}))

            if specifier == 'character':
                if Character.objects.filter(pk=pk).exists():
                    return HttpResponseRedirect(reverse('roster_character') + '?' + urlencode({'id': pk}))

    # Return 404 if any of the checks fail
    response = render(request, '404.html')
    response.status_code = 404
    return response


# Ajax
def ajax_autocomplete_search(request):
    if request.is_ajax():
        # Get search string
        keyword = request.GET.get('search', '').capitalize()

        # Get all specializations and characters whose name contains the keyword
        specializations = Specialization.objects.filter(name__contains=keyword)
        characters = Character.objects.filter(name__contains=keyword)

        # Prepare names for autocomplete
        names = []

        for specialization in specializations:
            names.append(
                [specialization.name, specialization.wow_class.name, specialization.id, str(specialization.icon),
                 'specialization'])

        for char in characters:
            names.append([char.name, char.id, str(char.specialization.icon), 'character'])

        # Encode results list to json data
        data = json.dumps(names)

        # Return HTTPResponse with autocomplete data
        mimetype = 'application/json'

        return HttpResponse(data, mimetype)

    # Return nothing if any of the checks fail
    return JsonResponse({})
