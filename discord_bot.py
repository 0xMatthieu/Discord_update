import os
import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

SERVER_NAME = os.getenv('DISCORD_SERVER_NAME')

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

client = MyClient()
client.run(TOKEN)
