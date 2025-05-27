# Flask AI Chat with Browser Automation

This is a Flask application that provides a chat interface with an AI powered by Foundry Local, along with browser automation capabilities. The application allows users to chat with an AI model and perform web browsing tasks, capturing screenshots of the results.

## Features

- Chat interface with the Phi-3.5-mini model via Foundry Local
- Browser automation using Playwright
- Screenshot capture and display
- Interactive UI for submitting browser automation tasks
- Modal image viewer for screenshots

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for cloning the repository)
- Foundry Local installed and configured

### Windows Installation

1. Clone or download this repository:
   ```
   git clone <repository-url>
   ```
   Or download and extract the ZIP file.

2. Navigate to the project directory:
   ```
   cd Foundry-Local-and-Browser-use
   ```

3. Create a virtual environment:
   ```
   python -m venv venv
   ```

4. Activate the virtual environment:
   ```
   venv\Scripts\activate
   ```

5. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

6. Install Playwright browsers:
   ```
   playwright install
   ```

7. Create the screenshots directory if it doesn't exist:
   ```
   mkdir -p static\screenshots
   ```

### Linux Installation

1. Clone or download this repository:
   ```bash
   git clone <repository-url>
   ```
   Or download and extract the ZIP file.

2. Navigate to the project directory:
   ```bash
   cd Foundry-Local-and-Browser-use
   ```

3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

4. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

5. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

6. Install Playwright browsers:
   ```bash
   playwright install
   ```

7. Create the screenshots directory if it doesn't exist:
   ```bash
   mkdir -p static/screenshots
   ```

### Alternative: Using Setup Script (Linux only)

If you're on Linux, you can use the provided setup script:

1. Make the script executable:
   ```bash
   chmod +x setup.sh
   ```

2. Run the setup script:
   ```bash
   ./setup.sh
   ```

## Running the Application

### Windows

1. Activate the virtual environment (if not already activated):
   ```
   venv\Scripts\activate
   ```

2. Start the Flask application:
   ```
   python app.py
   ```

3. Open your browser and navigate to `http://localhost:5000`

### Linux

1. Activate the virtual environment (if not already activated):
   ```bash
   source venv/bin/activate
   ```

2. Start the Flask application:
   ```bash
   python app.py
   ```
   
   Or use the run script if available:
   ```bash
   ./run.sh
   ```

3. Open your browser and navigate to `http://localhost:5000`

## Usage

1. On the home page, choose between the chat interface or browser automation
2. In the browser automation interface:
   - Enable browser automation by checking the checkbox
   - Enter a browser task (e.g., "Explore GitHub trends", "Browse Reddit for machine learning")
   - Enter your message/question
   - Click "Send" to submit both your message and the browser task
   - View the results, including screenshots of the browser automation

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
- `requirements.txt`: List of Python dependencies

## Troubleshooting

### Windows

- If you encounter issues with Playwright, try running:
  ```
  playwright install-deps
  ```

- If you get permission errors when creating directories, run your command prompt or PowerShell as administrator.

### Linux

- If you encounter issues with Playwright, ensure you have the necessary dependencies:
  ```bash
  sudo apt update
  sudo apt install -y libgbm-dev libxkbcommon-x11-0 libgtk-3-0 libasound2
  playwright install-deps
  ```

- If you get permission errors, check your file permissions:
  ```bash
  chmod -R 755 .
  ```

## Notes

- The application uses the Phi-3.5-mini model via Foundry Local
- Browser automation runs with visible browser windows (headless=False)
- Screenshots are stored in the `static/screenshots` directory