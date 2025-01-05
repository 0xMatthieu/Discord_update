#!/usr/bin/env python3

import os
import asyncio
import sqlite3
from collections import defaultdict
from discord_bot import getter_bot
from dotenv import load_dotenv

load_dotenv()
stored_messages = defaultdict(set)
CHANNEL_IDS = os.getenv('DISCORD_CHANNEL_IDS').split('/')

# Initialize SQLite database
conn = sqlite3.connect('messages.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        channel_id TEXT,
        channel_name TEXT,
        message_id TEXT PRIMARY KEY,
        sender_id TEXT,
        sender_name TEXT,
        content TEXT,
        reply_to TEXT,
        created_at TEXT
    )
''')
conn.commit()

async def get_last_messages(bot, channel_id: int, limit: int = 10):
    channel = bot.get_channel(int(channel_id))
    if channel:
        messages = []
        async for message in channel.history(limit=limit):
            print(message)
            if message.id not in stored_messages[channel_id]:
                stored_messages[channel_id].add(message.id)
                reply_to = message.reference.message_id if message.reference else None
                c.execute('''
                    INSERT OR IGNORE INTO messages (channel_id, channel_name, message_id, sender_id, sender_name, 
                    content, reply_to, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (channel_id, channel.name, message.id, message.author.id, message.author.name,
                      message.content, reply_to, message.created_at))
                conn.commit()
                messages.append(message.content)
        print('\n'.join(messages))
    else:
        print(f"Channel with ID {channel_id} not found.")

async def display_channel_messages(channel_id: str, limit: int = 3):
    c.execute('''
        SELECT content FROM messages
        WHERE channel_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    ''', (channel_id, limit))
    rows = c.fetchall()
    for row in rows:
        print(row[0])


async def test_db():
    print(f'run db test task')
    bot = await getter_bot()
    await get_last_messages(bot=bot, channel_id=int(CHANNEL_IDS[0]), limit=3)
    await display_channel_messages(channel_id=CHANNEL_IDS[0], limit=3)

