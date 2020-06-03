from django.shortcuts import render
from .utils import get_classes
from .models import Specialization


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
    pass


def search(request):
    pass


# Ajax
def ajax_autocomplete_search(request):
    pass
