from discord_bot import run_bot, ready_event

def start_discord_bot():
    run_bot()
    ready_event.wait()  # Wait until the bot is ready
    print("Bot is ready, proceeding with main program.")

if __name__ == "__main__":
    start_discord_bot()
