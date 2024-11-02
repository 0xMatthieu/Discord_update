import asyncio
from discord_bot import run_bot

async def run_until_complete():
    await run_bot()
    print("Bot has completed its tasks.")

if __name__ == "__main__":
    asyncio.run(run_until_complete())
