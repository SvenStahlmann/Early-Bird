from django.shortcuts import render
from .utils import get_classes
from .models import Specialization, Character


def overview(request):
    if request.method == 'GET':
        if request.GET.get('specialization'):
            specialization_id = request.GET.get('specialization')
            if Specialization.objects.filter(pk=specialization_id).exists():
                return render(request, 'roster/overview.html', {'classes': get_classes(), 'specialization': Specialization.objects.get(pk=specialization_id)})

    # Return 404 if any of the checks fail
    response = render(request, '404.html')
    response.status_code = 404
    return response


def character(request):
    if request.method == 'GET':
        if request.GET.get('character'):
            character_id = request.GET.get('character')
            if Character.objects.filter(pk=character_id).exists():
                return render(request, 'roster/character.html', {'classes': get_classes(), 'character': Character.objects.get(pk=character_id)})

    # Return 404 if any of the checks fail
    response = render(request, '404.html')
    response.status_code = 404
    return response


def search(request):
    pass


# Ajax
def ajax_autocomplete_search(request):
    pass
