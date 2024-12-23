#!/usr/bin/env python3

import os
import discord
import asyncio
import threading
from collections import defaultdict
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext import tasks

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

SERVER_NAMES = os.getenv('DISCORD_SERVER_NAMES').split('/')
CHANNEL_IDS = os.getenv('DISCORD_CHANNEL_IDS').split('/')
print(f'SERVER_NAMES: {SERVER_NAMES}')

description = '''A bot to get the last messages from a channel and made analysis on it.
It will not post any message, only read the last messages.
'''

bot = commands.Bot(command_prefix='?', description=description, self_bot=True)
stored_messages = defaultdict(set)

ready_event = asyncio.Event()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    ready_event.set()  # Signal that the bot is ready
    #await list_guilds()
    #await list_servers()
    print(f'on ready done')

async def list_servers():
    print("Listing all available servers and their channels:")
    for guild in bot.guilds:
        if guild.name in SERVER_NAMES:
            print(f'Server: {guild.name}')
            for channel in guild.channels:
                print(f'  - Channel: {channel.name} (ID: {channel.id})')

async def list_guilds():
    """Print all guilds the bot is a member of."""
    print("Listing all available servers:")
    for guild in bot.guilds:
        print(f'- {guild.name}')

async def get_last_messages(channel_id: int, limit: int = 10):
    channel = bot.get_channel(int(channel_id))
    if channel:
        messages = []
        async for message in channel.history(limit=limit):
            messages.append(message.content)
        print('\n'.join(messages))
        messages = []
        async for message in channel.history(limit=limit):
            messages.append(message.content)
        print('\n'.join(messages))
    else:
        print(f"Channel with ID {channel_id} not found.")

async def fetch_and_store_messages():
    for channel_id in CHANNEL_IDS:
        channel = bot.get_channel(int(channel_id))
        if channel:
            async for message in channel.history(limit=100):
                if message.id not in stored_messages[channel_id]:
                    stored_messages[channel_id].add(message.id)
                    # Store message content or any other relevant data
                    print(f"Stored message from {channel.name}: {message.content}")

async def periodic_message_fetch(interval_minutes=10):
    while True:
        await fetch_and_store_messages()
        await asyncio.sleep(interval_minutes * 60)

@tasks.loop(seconds=5)  # task runs every 60 seconds
async def test(self):
    print(f'run background task')
    await get_last_messages("1300515004000370688", 3)

async def run_bot():
    await bot.start(TOKEN)

