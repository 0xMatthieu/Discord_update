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

# Initialize SQLite database
conn = sqlite3.connect('messages.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        channel_id TEXT,
        message_id TEXT PRIMARY KEY,
        sender TEXT,
        content TEXT,
        reply_to TEXT
    )
''')
conn.commit()

async def run_bot():
    await bot.start(TOKEN)

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
            if message.id not in stored_messages[channel_id]:
                stored_messages[channel_id].add(message.id)
                reply_to = message.reference.message_id if message.reference else None
                c.execute('''
                    INSERT OR IGNORE INTO messages (channel_id, message_id, sender, content, reply_to)
                    VALUES (?, ?, ?, ?, ?)
                ''', (channel_id, message.id, str(message.author), message.content, reply_to))
                conn.commit()
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

async def background_task():
    print(f'run background task')
    await get_last_messages("1300515004000370688", 3)

async def test_fetch_last_messages(channel_id: str, limit: int = 3):
    c.execute('''
        SELECT content FROM messages
        WHERE channel_id = ?
        ORDER BY message_id DESC
        LIMIT ?
    ''', (channel_id, limit))
    rows = c.fetchall()
    for row in rows:
        print(row[0])
    await bot.start(TOKEN)

