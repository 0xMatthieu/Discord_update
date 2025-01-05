import asyncio
from discord_bot import run_bot, ready_event, test_standard
from discord_db_mgnt import test_db

async def start_discord_bot():
    bot_task = asyncio.create_task(run_bot())
    await ready_event.wait()  # Wait until the bot is ready
    print("Bot is ready, proceeding with main program.")
    #await test_db()  # Call the test function
    await test_standard()
    # await bot_task  # Ensure the bot task completes

if __name__ == "__main__":
    asyncio.run(start_discord_bot())
    print("done")
