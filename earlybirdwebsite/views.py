from django.shortcuts import render


def test(request):
    return render(request, 'raids/base.html')


def index(request):
    return render(request, 'index.html')
