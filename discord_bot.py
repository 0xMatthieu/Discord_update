#!/usr/bin/env python3

import os
import asyncio
import sqlite3
from collections import defaultdict
from dotenv import load_dotenv
from discord.ext import commands

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

async def run_bot():
    await bot.start(TOKEN)

async def getter_bot():
    return bot

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
            print(message)
            if message.id not in stored_messages[channel_id]:
                reply_to = message.reference.message_id if message.reference else None
                message_data = (channel_id, channel.name, message.id, message.author.id, message.author.name,
                                message.content, reply_to, message.created_at)
                stored_messages[channel_id].add(message_data)
                messages.append(message.content)
        print('\n'.join(messages))
    else:
        print(f"Channel with ID {channel_id} not found.")


async def display_stored_messages_with_field_names():
    field_names = [
        "Channel ID", "Channel Name", "Message ID", "Author ID", "Author Name",
        "Message Content", "Reply To", "Created At"
    ]

    for channel_id, messages in stored_messages.items():
        print(f"Channel ID: {channel_id}")
        for message_data in messages:
            print("  Message Data:")
            for field_name, field_value in zip(field_names, message_data):
                print(f"    {field_name}: {field_value}")

async def test_standard():
    print(f'run background task')
    await get_last_messages("1300515004000370688", 3)
    await display_stored_messages_with_field_names()



