from django.shortcuts import render
from django.http import HttpResponse
from . import bot


# Create your views here.
def start_bot(request):

    bot.DiscThread()

    return HttpResponse("Discord Bot started!")
