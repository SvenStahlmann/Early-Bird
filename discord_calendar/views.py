from django.shortcuts import render
from django.http import HttpResponse
from . import bot


# Create your views here.
def start_bot(request):
    if request.user.is_superuser:
        bot.DiscThread()

        return HttpResponse("Discord Bot started!")

    else:
        response = render(request, '404.html')
        response.status_code = 404
        return response
