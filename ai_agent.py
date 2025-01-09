import openai
from dotenv import load_dotenv
import os

from discord_db_mgnt import stored_messages

load_dotenv()
from smolagents.agents import ToolCallingAgent, CodeAgent
from smolagents import tool, LiteLLMModel, ManagedAgent
from typing import Optional
from discord_bot import get_last_messages
import asyncio

# Initialize the OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

model = LiteLLMModel(model_id="gpt-4o")

@tool
def summarize_a_channel(channel_id: str, limit: Optional[int] = 10) -> str:
    """
    get messages from a channel and returns a summary of what have been discussed

    Args:
        channel_id: as the name suggests, it is the id of requested channel. It could be str or int
        limit: optional arg to specify number of messages to retrieve
    """
    messages = asyncio.run(get_last_messages(channel_id=int(channel_id), limit=limit))
    output = f"""## channel {channel_id} \n"""
    for message_data in messages[int(channel_id)]:
        author_name = message_data[4]
        message_content = message_data[5]
        output = output + f"""author {author_name} said: {message_content} \n """

    #print(output)
    return output

agent = ToolCallingAgent(tools=[summarize_a_channel], model=model, max_iterations=1)

managed_discord_agent = ManagedAgent(
    agent=agent,
    name="summarize",
    description="""You will be tasked to read messages and provide a summary. 
    Focus on major points about crypto and leave daily discussions""",
)

manager_agent = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[managed_discord_agent],
    additional_authorized_imports=["asyncio", "discord_bot"],
)

def call_agent(query: str, simple_agent: Optional[bool] = True):
    if simple_agent:
        print(agent.run(query))
    else:
        print(manager_agent.run(query))