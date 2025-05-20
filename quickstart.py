import openai
from foundry_local import FoundryLocalManager

# Use an alias to select the most suitable model
alias = "phi-4"

# Start Foundry Local and load the model
manager = FoundryLocalManager(alias)

# Connect OpenAI client to the local Foundry endpoint
client = openai.OpenAI(
    base_url=manager.endpoint,
    api_key=manager.api_key  # Not required for local usage
)

# Generate a response from the local model
response = client.chat.completions.create(
    model=manager.get_model_info(alias).id,
    max_tokens=4096,
    messages=[{"role": "user", "content": "What is the golden ratio?"}]
)
print(response.choices[0].message.content)