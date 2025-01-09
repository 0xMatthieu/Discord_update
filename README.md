# Discord_update

A bot to sum up last messages on a given Discord server.

## Architecture

The project is structured into several modules, each responsible for different functionalities:

- **discord_bot.py**: This module handles the connection to Discord using the Discord API. It manages the bot's lifecycle, including starting the bot, listing servers and channels, and retrieving messages from channels.

- **discord_db_mgnt.py**: This module manages the storage of messages in a SQLite database. It provides functions to fetch and display messages from the database.

- **ai_agent.py**: This module integrates with OpenAI's API to provide AI-driven functionalities, such as summarizing messages from a Discord channel.

## Key Functions

### discord_bot.py

- `run_bot()`: Starts the Discord bot.
- `start_discord_bot()`: Initializes and runs the bot, waiting for it to be ready.
- `getter_bot()`: Returns the bot instance.
- `list_servers()`: Lists all available servers and their channels.
- `get_last_messages(channel_id, limit)`: Retrieves the last messages from a specified channel.

### discord_db_mgnt.py

- `get_last_messages(bot, channel_id, limit)`: Fetches the last messages from a channel and stores them in the database.
- `display_channel_messages(channel_id, limit)`: Displays messages from the database for a specified channel.

### ai_agent.py

- `summarize_a_channel(channel_id, limit)`: Summarizes messages from a specified channel using AI.
- `call_agent(query, simple_agent)`: Executes an AI agent to process a query.

## Usage

To use the bot, ensure you have the necessary environment variables set in a `.env` file, including `DISCORD_TOKEN`, `DISCORD_SERVER_NAMES`, and `DISCORD_CHANNEL_IDS`. Run the bot using the appropriate Python command.
