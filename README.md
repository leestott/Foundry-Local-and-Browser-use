# AI-Powered Browser Automation with Foundry Local

A sophisticated Flask application that combines Foundry Local AI models with Playwright browser automation to create intelligent, adaptive web browsing experiences. The system uses AI for task planning, step-by-step execution, and smart CAPTCHA avoidance.

## Key Features

### **AI-Driven Automation**
- **Dynamic Task Planning**: AI analyzes natural language tasks and creates detailed step-by-step automation plans
- **Intelligent Action Generation**: Real-time decision making for browser actions based on page context
- **Adaptive Execution**: Smart responses to different website layouts and content
- **Context-Aware Navigation**: AI understands page content to make optimal choices

### **Advanced CAPTCHA Protection**
- **Multi-Pattern Detection**: Detects various CAPTCHA types (reCAPTCHA, hCAPTCHA, Cloudflare, etc.)
- **Smart Evasion**: Automatically navigates to alternative sites when CAPTCHAs are encountered
- **Keyword Analysis**: Text-based CAPTCHA detection for comprehensive coverage
- **Seamless Fallbacks**: Continues automation on privacy-focused alternatives

### **Comprehensive Screenshot System**
- **Step-by-Step Documentation**: Before/after screenshots for every automation step
- **Visual Progress Tracking**: Complete visual record of the automation process
- **Interactive Web Viewer**: Click to expand screenshots in the browser interface
- **Organized Storage**: Timestamped screenshots with unique session IDs

### **Intelligent Execution**
- **Real-Time Planning**: AI generates 4-8 step plans tailored to each specific task
- **Error Recovery**: Graceful handling of failures with continued execution
- **Progressive Actions**: NAVIGATE, FILL, CLICK, PRESS, SCROLL, WAIT, EXTRACT, SCREENSHOT
- **Success Verification**: AI validates task completion at each step

## Architecture

### **Core Components**
- **`app.py`** - Main Flask application with AI integration
- **`config.py`** - Configuration for AI models and Flask settings
- **Foundry Local Integration** - Local AI model for planning and actions
- **Playwright Automation** - Headless browser control for actual web interactions

### **AI Workflow**
1. **Task Analysis** - AI breaks down natural language requests into actionable steps
2. **Dynamic Planning** - Generate 4-8 specific steps with context awareness
3. **Action Generation** - AI determines exact browser actions (selectors, inputs, clicks)
4. **Execution Monitoring** - Real-time adaptation based on page responses
5. **CAPTCHA Handling** - Automatic detection and alternative routing

## 🚀 Quick Start

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
playwright install
```

### **2. Setup Foundry Local**
- Ensure Foundry Local is installed and running
- Configure model access
- Verify connection to local AI endpoint

### **3. Start the Application**
```bash
python app.py
```

### **4. Access Web Interface**
```
http://127.0.0.1:5000
```

## 📂 Project Structure

```
├── app.py                    # Main Flask application with AI automation
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── templates/              # HTML templates
│   ├── index.html         # Home page with interface selection
│   ├── chat.html          # Direct AI chat interface
│   └── browser.html       # Browser automation interface
└── static/
    └── screenshots/       # Generated automation screenshots
```

## 🔧 API Endpoints

### **Core Interfaces**
- `GET /` - Home page with interface selection
- `GET /chat` - Direct AI chat interface
- `GET /browser` - Browser automation interface

### **AI & Automation**
- `POST /generate` - Generate AI responses for chat
- `POST /automate` - Execute browser automation with AI planning

### **Advanced Features**
- **AI Task Planning** - Converts natural language to browser actions
- **Dynamic Step Execution** - Real-time action generation based on page state
- **CAPTCHA Detection** - Multi-layer detection with smart alternatives
- **Screenshot Documentation** - Complete visual automation records

## Example Tasks

The AI can handle complex automation tasks like:

```
"Search for Python programming tutorials on Google"
"Find the latest news about artificial intelligence"  
"Look up information about climate change on Wikipedia"
"Browse Reddit for technology discussions"
"Check the weather forecast for New York"
"Find open source projects on GitHub"
```

## AI Integration

### **Model Configuration**
- **Default Model**: Phi-4 via Foundry Local
- **Planning Mode**: Low temperature (0.3) for consistent planning
- **Action Mode**: Very low temperature (0.2) for precise actions
- **Context Awareness**: Analyzes page content for smart decisions

### **Intelligent Features**
- **Task Understanding**: Converts natural language to automation steps
- **Selector Intelligence**: AI generates appropriate CSS selectors
- **Context Adaptation**: Actions adapt to different website layouts
- **Error Recovery**: Smart fallbacks when actions fail

## CAPTCHA Handling

### **Detection Methods**
- **Selector-Based**: Multiple CSS selector patterns
- **Content Analysis**: Keyword detection in page text
- **Visual Verification**: Screenshot analysis capabilities
- **Behavioral Patterns**: Recognition of common CAPTCHA flows

### **Avoidance Strategies**
- **Alternative Sites**: DuckDuckGo, Bing, Yahoo, StartPage
- **Privacy-Focused**: Preference for CAPTCHA-resistant platforms
- **Smart Routing**: Automatic redirection when CAPTCHAs detected
- **Session Management**: Clean browser profiles to avoid triggers

## Screenshot System

### **Automated Documentation**
- **Before/After Shots**: Every action documented visually
- **Session Tracking**: Unique IDs for organized screenshot sets
- **Step Descriptions**: AI-generated descriptions for each screenshot
- **Web Interface**: Interactive viewing with click-to-expand

### **Storage & Organization**
- **Timestamped Files**: Easy chronological organization
- **Session Grouping**: Screenshots grouped by automation session
- **Metadata Integration**: Descriptions and context stored with images
- **Cleanup Tools**: Automatic management of old screenshots

## 🔧 Configuration

### **AI Settings** (`config.py`)
```python
# AI Model Configuration
AI_CONFIG = {
    'default_model': 'phi-4',           # Foundry Local model
    'max_tokens': 4096,                 # Response length limit
    'temperature': 0.7,                 # Response creativity
    'timeout': 30                       # Request timeout
}
```

### **Flask Settings**
```python
# Flask Configuration  
FLASK_CONFIG = {
    'debug': True,                      # Development mode
    'host': '127.0.0.1',               # Server host
    'port': 5000                       # Server port
}
```

## Dependencies

- **Flask** - Web framework for the interface
- **Playwright** - Browser automation engine
- **OpenAI** - API client compatible with Foundry Local
- **Foundry Local SDK** - Local AI model management

## Requirements

- Python 
- Foundry Local installed and configured
- Playwright browsers installed (`playwright install`)

## Usage Notes

- **Browser Visibility**: Automation runs in non-headless mode for demonstration
- **CAPTCHA Awareness**: System automatically detects and avoids CAPTCHAs
- **AI Planning**: Each task gets a custom AI-generated execution plan
- **Screenshot Storage**: All automation steps are visually documented

## 📄 License

MIT License - Open source and free to modify for your automation needs.