from django.shortcuts import render
from .utils import get_instances


def page(request):
    return render(request, 'raids/base.html', {'instances': get_instances()})
