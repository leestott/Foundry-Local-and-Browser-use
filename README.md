# Foundry Local and Browser Use

This repository demonstrates how to use the Foundry Local SDK with AI models for both local execution and browser-based interactions. It provides several examples of integrating local AI models with web applications and browser automation.

## Overview

This project showcases three main use cases:
1. **Quickstart**: Simple command-line interaction with local AI models
2. **Web Application**: Flask-based web interface for interacting with AI models
3. **Browser Automation**: Using AI models with browser automation capabilities

## Prerequisites

- Python 3.8+
- Foundry Local installed and configured
- AI models accessible via Foundry Local (e.g., phi-3.5-mini, phi-4)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Foundry-Local-and-Browser-use.git
cd Foundry-Local-and-Browser-use

# Install dependencies
pip install -r requirements.txt
```

## Components

### 1. Quickstart Example (`quickstart.py`)

Demonstrates the most basic usage of Foundry Local for running AI inference:

```python
import openai
from foundry_local import FoundryLocalManager

# Initialize with your preferred model
alias = "phi-4"
manager = FoundryLocalManager(alias)

# Connect to the local endpoint
client = openai.OpenAI(base_url=manager.endpoint, api_key=manager.api_key)

# Generate a response
response = client.chat.completions.create(
    model=manager.get_model_info(alias).id,
    max_tokens=4096,
    messages=[{"role": "user", "content": "What is the golden ratio?"}]
)
print(response.choices[0].message.content)
```

### 2. Web Application (`app.py`)

A Flask web application that provides a chat interface for interacting with AI models:

- Serves a responsive web interface
- Processes user prompts via API endpoints
- Returns AI-generated responses to the client

To run the web application:

```bash
python app.py
```

Then open your browser and navigate to `http://localhost:5000`

### 3. Browser Automation (`browser.py`)

Demonstrates using AI models with browser automation to perform tasks online:

```python
import asyncio
import openai
from browser_use import Agent
from foundry_local import FoundryLocalManager

# Initialize with your preferred model
alias = "phi-4"
manager = FoundryLocalManager(alias)

# Run an automated browser task
async def main():
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3",
        llm=openai.OpenAI(base_url=manager.endpoint, api_key=manager.api_key),
    )
    await agent.run()

asyncio.run(main())
```

## Dependencies

- `openai`: Client library for interacting with OpenAI-compatible APIs
- `foundry-local-sdk`: SDK for running AI models locally via Foundry
- `browser-use`: Library for browser automation with AI
- `open-webui`: Web UI components
- `Flask`: Web framework for the chat application

## Project Structure

```
├── app.py              # Flask web application
├── browser.py          # Browser automation example
├── quickstart.py       # Basic usage example
├── requirements.txt    # Project dependencies
├── static/             # Static assets for the web app
└── templates/          # HTML templates
    └── index.html      # Main chat interface
```

## License

[Specify your license here]

## Acknowledgments

- Foundry Local team for providing the local AI execution environment
- Browser Use library developers