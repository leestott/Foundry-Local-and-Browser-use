# Flask AI Chat with Browser Automation

This is a Flask application that provides a chat interface with an AI powered by Foundry Local, along with browser automation capabilities. The application allows users to chat with an AI model and perform web browsing tasks, capturing screenshots of the results.

## Features

- Chat interface with the Phi-3.5-mini model via Foundry Local
- Browser automation using Playwright
- Screenshot capture and display
- Interactive UI for submitting browser automation tasks
- Modal image viewer for screenshots

## Installation

1. Run the setup script to install dependencies:

```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Create a virtual environment
- Install Python dependencies
- Install Playwright browsers
- Create required directories

## Usage

1. Start the Flask application:

```bash
./run.sh
```

2. Open your browser and navigate to `http://localhost:5000`
3. Enable browser automation by checking the checkbox
4. Enter a browser task (e.g., "Explore GitHub trends", "Browse Reddit for machine learning")
5. Enter your message/question
6. Click "Send" to submit both your message and the browser task
7. View the results, including screenshots of the browser automation

## Browser Task Examples

- "Go to GitHub and explore trending repositories"
- "Browse Reddit for machine learning"
- "Check weather forecast on Weather.gov"
- "Find information about quantum computing on Wikipedia"
- "Visit https://github.com"

## Project Structure

- `app.py`: Main Flask application
- `templates/`: HTML templates for the web interface
- `static/screenshots/`: Directory for storing screenshots
- `run.sh`: Script to run the application
- `setup.sh`: Script to set up the environment
- `requirements.txt`: List of Python dependencies
