# AI-Powered Browser Automation with Intelligent Planning

This is a Flask application that provides an advanced chat interface with AI-powered browser automation. The system uses local AI models via Foundry Local to intelligently plan and execute web browsing tasks with sophisticated CAPTCHA detection and step-by-step reasoning.

## 🚀 Key Features

### 🧠 AI-Powered Automation
- **Dynamic Task Planning**: AI analyzes tasks and creates custom step-by-step plans
- **Intelligent Action Generation**: AI determines the best browser actions based on page context
- **Adaptive Execution**: Real-time decision making that adapts to different websites
- **Context-Aware Navigation**: Understands page content to make smart choices

### 🛡️ Advanced CAPTCHA Protection
- **Multi-Pattern Detection**: Detects various CAPTCHA types (reCAPTCHA, hCAPTCHA, Cloudflare, etc.)
- **Smart Evasion**: Automatically navigates to alternative sites when CAPTCHAs are encountered
- **Keyword Analysis**: Text-based CAPTCHA detection for comprehensive coverage
- **Seamless Fallbacks**: Continues automation on privacy-focused alternatives

### 🎯 Goal-Oriented Execution
- **Step-by-Step Breakdown**: Complex tasks divided into manageable steps
- **Real-Time Logging**: Detailed progress tracking with emojis and clear status updates
- **Error Recovery**: Graceful handling of failures with continued execution
- **Screenshot Documentation**: Before/after screenshots for each step

### 🔒 Privacy-Focused Approach
- **No Google/Amazon**: Automatically redirects to privacy-friendly alternatives
- **DuckDuckGo Integration**: Default search engine for better privacy
- **eBay over Amazon**: Alternative marketplace for shopping tasks
- **Enhanced Security**: Multiple CAPTCHA detection layers

### 📸 Enhanced Screenshot System
- **Intelligent Capture**: Screenshots at key decision points
- **Step Documentation**: Visual proof of each automation step
- **Modal Viewer**: Interactive image viewing in the web interface
- **Organized Storage**: Timestamped and categorized screenshot management

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

6. Create the screenshots directory if it doesn't exist:
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

6. Create the screenshots directory if it doesn't exist:
   ```bash
   mkdir -p static/screenshots
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
   

3. Open your browser and navigate to `http://localhost:5000`

## Usage

1. On the home page, choose between the chat interface or browser automation
2. In the browser automation interface:
   - Enable browser automation by checking the checkbox
   - Enter a browser task (e.g., "Explore GitHub trends", "Browse Reddit for machine learning")
   - Enter your message/question
   - Click "Send" to submit both your message and the browser task
   - View the results, including screenshots of the browser automation

## 📋 How It Works

### 1. AI Task Analysis
When you submit a task, the AI:
- Analyzes the request to understand the goal
- Creates a detailed step-by-step execution plan
- Considers potential obstacles and alternative approaches
- Generates 4-8 specific, actionable steps

### 2. Intelligent Execution
For each step, the AI:
- Examines the current page context (URL, title, content)
- Determines the optimal browser action (navigate, click, fill, etc.)
- Executes the action with appropriate timing and error handling
- Adapts to unexpected page layouts or elements

### 3. CAPTCHA Protection
The system automatically:
- Scans for multiple CAPTCHA patterns and keywords
- Takes screenshots when CAPTCHAs are detected
- Navigates to privacy-focused alternative sites
- Continues the task flow seamlessly

### 4. Action Types
The AI can execute these browser actions:
- `NAVIGATE`: Go to specific URLs
- `FILL`: Enter text in input fields
- `CLICK`: Click on page elements
- `PRESS`: Use keyboard shortcuts
- `SCROLL`: Navigate page content
- `WAIT`: Pause for loading/timing
- `EXTRACT`: Gather text information
- `SCREENSHOT`: Document progress

## 🎯 Example AI Workflows

### Search Task: "Find information about electric cars"
```
📋 AI GENERATED TASK PLAN:
   1. Navigate to a reliable search engine
   2. Enter search query for electric vehicle information
   3. Submit the search and wait for results
   4. Click on the most informative result
   5. Read through the article content
   6. Scroll to gather additional details
   7. Verify information quality and completeness
```

### Shopping Task: "Find laptops under $1000"
```
📋 AI GENERATED TASK PLAN:
   1. Navigate to eBay marketplace
   2. Enter search criteria for affordable laptops
   3. Apply price filters and sorting options
   4. Browse through relevant product listings
   5. Click on highly-rated products
   6. Compare specifications and pricing
   7. Document findings for decision making
```

## Project Structure

- `app.py`: Main Flask application
- `templates/`: HTML templates for the web interface
- `static/screenshots/`: Directory for storing screenshots
- `requirements.txt`: List of Python dependencies

## 🔧 Troubleshooting

### Common Issues

**AI Planning Failures**
- Ensure Foundry Local is running and accessible
- Check that the Phi-3.5-mini model is properly loaded
- Verify network connectivity for local model inference

**Browser Automation Issues**
- Run `playwright install` to ensure browsers are installed
- Check that the display is available (not running headless improperly)
- Verify sufficient disk space for screenshots

**CAPTCHA Problems**
- CAPTCHAs are automatically handled with alternative sites
- If persistent issues occur, the system will log detailed error messages
- Check console output for specific CAPTCHA detection patterns

**Screenshot Issues**
- Ensure `static/screenshots/` directory exists and is writable
- Screenshots are automatically git-ignored
- Check available disk space for image storage


### Performance Optimization

**Speed Adjustments**
- Modify timing delays in `execute_ai_generated_step` for faster/slower execution
- Adjust AI token limits for quicker planning (may reduce plan quality)
- Use headless mode for faster automation (modify `headless=False` to `headless=True`)

**Resource Management**
- Screenshots are automatically cleaned up by session
- Monitor disk usage in `static/screenshots/` directory
- Consider implementing screenshot rotation for long-running instances

## 📊 Monitoring and Logs

The system provides extensive logging:
- **🧠 AI Analysis**: Task planning and reasoning
- **📋 Generated Plans**: Step-by-step execution plans
- **🎯 Step Execution**: Real-time progress updates
- **🤖 AI Actions**: Specific browser actions taken
- **🛡️ CAPTCHA Detection**: Security measure notifications
- **✅ Completion Status**: Success/failure indicators
- **📸 Screenshot Tracking**: Image capture confirmations

## 📝 Notes

### AI Model Configuration
- Uses Phi-3.5-mini model via Foundry Local for intelligent planning
- Local inference ensures privacy and no external API dependencies
- Model can be switched by modifying the `alias` variable in `app.py`

### Browser Behavior
- Runs with visible browser windows (`headless=False`) for transparency
- Implements smart timing delays for reliable automation
- Automatically handles dynamic content loading and page transitions

### Privacy and Security
- No data sent to external services (fully local AI processing)
- Avoids Google and Amazon by default for enhanced privacy
- CAPTCHA protection prevents bot detection and blocking
- All screenshots stored locally and git-ignored

### Screenshot Management
- Images stored in `static/screenshots/` with session-based organization
- Automatic before/after documentation for debugging
- Files automatically excluded from Git tracking
- Consider periodic cleanup for disk space management

### Customization Options
- Modify AI prompts in planning functions for different behavior
- Adjust timing delays for speed vs. reliability trade-offs
- Customize CAPTCHA detection patterns for specific sites
- Add new action types for specialized automation needs

---

## 🚀 Recent Updates

**v2.0 - AI-Powered Intelligence**
- ✅ Dynamic AI task planning and execution
- ✅ Intelligent action generation based on page context
- ✅ Advanced CAPTCHA detection and evasion
- ✅ Step-by-step execution with detailed logging
- ✅ Privacy-focused site alternatives (DuckDuckGo, eBay)
- ✅ Enhanced screenshot management with Git ignore
- ✅ Real-time progress tracking and error recovery
- ✅ Context-aware browser automation