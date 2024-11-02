#!/usr/bin/env python3

import os
import discord
from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

SERVER_NAME = os.getenv('DISCORD_SERVER_NAME')

description = '''A bot to get the last messages from a channel and made analysis on it.
It will not post any message, only read the last messages.
'''

bot = commands.Bot(command_prefix='?', description=description, self_bot=True)

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
        self.list_servers()

    def list_servers(self):
        print("Listing all available servers:")
        for guild in self.guilds:
            print(f'- {guild.name}')

    async def get_last_messages(self, channel, limit=10):
        messages = []
        async for message in channel.history(limit=limit):
            messages.append(message.content)
        return messages

intents = Intents.default()
intents.message_content = True  # Enable the message content intent

client = MyClient(intents=intents)
client.run(TOKEN)
