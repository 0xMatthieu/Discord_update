import os
import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
        for guild in self.guilds:
            print(f'Guild: {guild.name}')
            for channel in guild.text_channels:
                print(f'Channel: {channel.name}')

    async def get_last_messages(self, channel, limit=10):
        messages = []
        async for message in channel.history(limit=limit):
            messages.append(message.content)
        return messages

client = MyClient()
client.run(TOKEN)
