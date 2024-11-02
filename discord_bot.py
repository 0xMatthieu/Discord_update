#!/usr/bin/env python3

import os
import discord
import asyncio
from collections import defaultdict
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

SERVER_NAMES = os.getenv('DISCORD_SERVER_NAMES').split(',')
CHANNEL_IDS = os.getenv('DISCORD_CHANNEL_IDS').split(',')

description = '''A bot to get the last messages from a channel and made analysis on it.
It will not post any message, only read the last messages.
'''


bot = commands.Bot(command_prefix='?', description=description, self_bot=True)
stored_messages = defaultdict(set)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await list_servers()

async def list_servers():
    print("Listing all available servers and their channels:")
    for guild in bot.guilds:
        if guild.name in SERVER_NAMES:
            print(f'Server: {guild.name}')
            for channel in guild.channels:
                print(f'  - Channel: {channel.name} (ID: {channel.id})')

@bot.command()
async def get_last_messages(ctx, limit: int = 10):
    messages = []
    async for message in ctx.channel.history(limit=limit):
        messages.append(message.content)
    await ctx.send('\n'.join(messages))

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

"""
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await list_servers()
    bot.loop.create_task(periodic_message_fetch())
"""
bot.run(TOKEN)
