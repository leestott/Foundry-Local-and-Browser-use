import asyncio
import openai
from browser_use import Agent
from foundry_local import FoundryLocalManager

# Use an alias to select the most suitable model
alias = "phi-4"

# Start Foundry Local and load the model
manager = FoundryLocalManager(alias)

async def main():
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3",
        llm=openai.OpenAI(
                base_url=manager.endpoint,
                api_key=manager.api_key  # Not required for local usage
            ),
    )
    await agent.run()

asyncio.run(main())