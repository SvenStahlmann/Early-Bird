# bot.py
import discord
from threading import Thread
from datetime import datetime
import re

from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from loot.models import RaidDay
from roster.models import Character
from .models import CalendarEntry
from . import utils
from earlybirdwebsite import settings

# TODO: do not create CalendarEntry object if reaction was less than 24h before RaidDay


class EbeDiscord(discord.Client):

    TOKEN = settings.DISCORD_TOKEN
    SERVER = settings.DISCORD_SERVER

    async def on_ready(self):

        for guild in self.guilds:

            if guild.name == self.SERVER:
                print(f'{self.user} has connected to Discord!')

    async def on_raw_reaction_add(self, payload):

        channel = self.get_channel(payload.channel_id)
        if channel.name == 'websiteplanung':

            # check if message was from Raid-Helper
            msg = await channel.fetch_message(payload.message_id)
            if len(msg.embeds) > 0:
                embed = msg.embeds[0].to_dict()

                # get event info - datetime
                match = re.search('until:(.*)- GMT', embed['footer']['text']).group(1)
                raid_date = match.replace(' @ ', ' ').strip()
                date_time = datetime.strptime(raid_date, '%d-%b-%Y %H:%M')
                # get event info - event name
                fields = embed['fields'][0]['value']
                event_name = re.findall('<:(.*?):', fields)
                event_name = utils.transform_discord_emoji_to_text(event_name)

                # create raid day if it does not exist
                raid_day, created = await sync_to_async(RaidDay.objects.get_or_create)(title=event_name, date=date_time)

                # create note that player reacted to the raid event
                try:
                    character = await sync_to_async(Character.objects.get)(name=payload.member.display_name)
                    await sync_to_async(CalendarEntry.objects.get_or_create)(character=character, raid_day=raid_day)
                except ObjectDoesNotExist:
                    print(f"Character {payload.member.display_name} does not exist.")


client = EbeDiscord()
Thread(target=client.run, args=(client.TOKEN,), daemon=True).start()
