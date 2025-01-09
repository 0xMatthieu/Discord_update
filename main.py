import asyncio
from discord_bot import ready_event, start_discord_bot
from ai_agent import call_agent
import os

async def init():
    await start_discord_bot()
    print("Bot has been started")

if __name__ == "__main__":
    """
    asyncio.run(init())
    print('bot started')
    """
    call_agent(query=f'can you summarize last 10 messages of channel {os.getenv('DISCORD_CHANNEL_IDS')}',
               simple_agent=False)
    print("done")
