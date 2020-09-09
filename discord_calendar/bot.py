# bot.py
import discord
from threading import Thread
import asyncio
from datetime import datetime, timedelta
import re

from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from loot.models import RaidDay
from roster.models import Character
from .models import CalendarEntry, LateSignUp
from . import utils
from earlybirdwebsite import settings


class EbeDiscord(discord.Client):

    TOKEN = settings.DISCORD_TOKEN
    SERVER = settings.DISCORD_SERVER

    async def on_ready(self):

        for guild in self.guilds:

            if guild.name == self.SERVER:
                print(f'{self.user} has connected to Discord!')

    async def on_raw_reaction_add(self, payload):

        channel = self.get_channel(payload.channel_id)
        if channel.name in ['mittwoch-raid', 'freitag-raid']:

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
                possible_character_names = payload.member.display_name.replace('|', '/').split('/')
                possible_character_names = [name.strip() for name in possible_character_names]

                # check if character exists in raid line up
                for char_name in possible_character_names:
                    try:
                        character = await sync_to_async(Character.objects.get)(name__iexact=char_name)

                        # check if character has already reacted to event before
                        try:
                            # character has already signed up - don't create a new entry
                            await sync_to_async(CalendarEntry.objects.get)(character=character, raid_day=raid_day)
                            return

                        except ObjectDoesNotExist:
                            # check if sign up was within time limit
                            if datetime.now() < (date_time - timedelta(days=1)):
                                await sync_to_async(CalendarEntry.objects.get_or_create)(character=character, raid_day=raid_day)
                                print(f"{char_name} signed up")
                            else:
                                await sync_to_async(LateSignUp.objects.get_or_create)(character=character, raid_day=raid_day)
                                print(f"{char_name} signed up late")
                    except ObjectDoesNotExist:
                        print(f"Character {char_name} does not exist.")


class DiscThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.start()

    async def starter(self):

        self.discord_client = EbeDiscord()
        await self.discord_client.start(EbeDiscord.TOKEN)

    def run(self):
        self.name = 'Discord.py'

        self.loop.create_task(self.starter())
        self.loop.run_forever()
