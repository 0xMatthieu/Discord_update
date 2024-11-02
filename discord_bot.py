#!/usr/bin/env python3

import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

SERVER_NAME = os.getenv('DISCORD_SERVER_NAME')

description = '''A bot to get the last messages from a channel and made analysis on it.
It will not post any message, only read the last messages.
'''

intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

bot = commands.Bot(command_prefix='?', description=description, self_bot=True, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    list_servers()

def list_servers():
    print("Listing all available servers:")
    for guild in bot.guilds:
        print(f'- {guild.name}')

@bot.command()
async def get_last_messages(ctx, limit: int = 10):
    messages = []
    async for message in ctx.channel.history(limit=limit):
        messages.append(message.content)
    await ctx.send('\n'.join(messages))

bot.run(TOKEN)
