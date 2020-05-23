from django.shortcuts import render


def test(request):
    return render(request, 'test.html')


def index(request):
    return render(request, 'index.html')
