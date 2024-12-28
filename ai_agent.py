import os
import openai
import sqlite3
from pydantic import BaseModel

# Load OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define a Pydantic model for the response
class SummaryResponse(BaseModel):
    channel_id: str
    summary: str

def summarize_channel_messages(channel_id: str) -> SummaryResponse:
    # Connect to the SQLite database
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()

    # Fetch messages from the database
    c.execute('''
        SELECT content FROM messages
        WHERE channel_id = ?
    ''', (channel_id,))
    messages = c.fetchall()

    # Concatenate messages into a single string
    content = " ".join([msg[0] for msg in messages])

    # Use OpenAI to summarize the content
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Summarize the following messages: {content}",
        max_tokens=150
    )

    # Extract the summary from the response
    summary = response.choices[0].text.strip()

    # Return the summary wrapped in a Pydantic model
    return SummaryResponse(channel_id=channel_id, summary=summary)
