import asyncio
from discord_bot import run_bot

async def start_discord_bot():
    await run_bot()
    print("Bot is ready, proceeding with main program.")

if __name__ == "__main__":
    asyncio.run(start_discord_bot())
    print("done")