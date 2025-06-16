import os
import asyncio
import time
import uuid
import base64
from flask import Flask, render_template, request, jsonify, send_from_directory
import openai
from foundry_local import FoundryLocalManager
from playwright.async_api import async_playwright
from pathlib import Path

# Create static directory for screenshots if it doesn't exist
Path("static/screenshots").mkdir(parents=True, exist_ok=True)

app = Flask(__name__)

# Store instances of the manager and client for reuse
manager = None
client = None
alias = "phi-3.5-mini"  # Default model alias

def get_openai_client():
    """Initialize the OpenAI client if needed and return it."""
    global manager, client
    
    if manager is None:
        manager = FoundryLocalManager(alias)
    
    if client is None:
        client = openai.OpenAI(
            base_url=manager.endpoint,
            api_key=manager.api_key  # Not required for local usage
        )
    
    return client

@app.route('/')
def index():
    """Render the home page with links to both interfaces."""
    return render_template('index.html')

@app.route('/chat')
def chat():
    """Render the chat interface."""
    return render_template('chat.html')

@app.route('/browser')
def browser():
    """Render the browser automation interface."""
    return render_template('browser.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Generate a response from the AI model."""
    global manager
    
    # Get user prompt
    data = request.json
    user_prompt = data.get('prompt', '')
    
    if not user_prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    client = get_openai_client()
    
    # Generate a response from the local model
    response = client.chat.completions.create(
        model=manager.get_model_info(alias).id,
        max_tokens=4096,
        messages=[{"role": "user", "content": user_prompt}]
    )
        
    # Extract the response content
    response_content = response.choices[0].message.content
    
    return jsonify({
        "response": response_content
    })

@app.route('/automate', methods=['POST'])
def automate():
    """Run browser automation task and return screenshots."""
    data = request.json
    browser_task = data.get('browserTask', '')
    
    if not browser_task:
        return jsonify({"error": "No browser task provided"}), 400
        
    try:
        # Run browser automation asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        screenshot_paths = loop.run_until_complete(run_browser_automation(browser_task))
    except Exception as e:
        return jsonify({"error": f"Browser automation failed: {str(e)}"}), 500
        
    # Prepare screenshot data for response
    screenshot_data = []
    for i, path in enumerate(screenshot_paths):
        with open(os.path.join("static", path), "rb") as f:
            img_data = base64.b64encode(f.read()).decode('utf-8')
            
            # Add descriptive metadata based on screenshot position
            description = ""
            if i == 0:
                description = "Initial page view"
            elif i == len(screenshot_paths) - 1:
                description = "Final result"
            else:
                description = f"Step {i+1}"
                
            screenshot_data.append({
                "path": path,
                "data": img_data,
                "description": description
            })
    
    return jsonify({
        "message": f"Completed browser task: {browser_task}",
        "screenshots": screenshot_data
    })

async def generate_task_plan_with_ai(task):
    """Use AI to analyze the task and create a step-by-step plan."""
    client = get_openai_client()
    
    planning_prompt = f"""
    You are an expert web automation planner. Analyze the following task and create a detailed step-by-step plan to accomplish it using a web browser.

    Task: "{task}"

    Consider these guidelines:
    - Break the task into 4-8 clear, actionable steps
    - Each step should be specific and measurable
    - Consider potential obstacles like CAPTCHAs, slow loading, or missing elements
    - Prefer privacy-focused alternatives (DuckDuckGo over Google, eBay over Amazon)
    - Include verification steps to ensure goals are achieved
    - End with a clear success criterion

    Return ONLY a numbered list of steps, nothing else. Example format:
    1. Navigate to the target website
    2. Enter search criteria in the search box
    3. Submit the search query
    4. Review and analyze the results
    5. Click on the most relevant result
    6. Capture and verify the information
    """

    try:
        response = client.chat.completions.create(
            model=manager.get_model_info(alias).id,
            max_tokens=512,
            messages=[{"role": "user", "content": planning_prompt}]
        )
        
        plan_text = response.choices[0].message.content.strip()
        
        # Parse the numbered steps into a list
        steps = []
        for line in plan_text.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('- ')):
                # Remove numbering and clean up
                step = line.split('.', 1)[-1].strip() if '.' in line else line.replace('- ', '').strip()
                if step:
                    steps.append(step)
        
        return steps if steps else [f"Navigate and explore: {task}"]
        
    except Exception as e:
        print(f"❌ AI planning failed: {e}")
        # Fallback to a simple generic plan
        return [
            f"Navigate to relevant website for: {task}",
            "Wait for page to load completely",
            "Interact with key elements on the page",
            "Capture important information",
            "Verify task completion"
        ]

async def generate_step_action_with_ai(step_description, current_url, task, page):
    """Use AI to determine what specific action to take for a step."""
    client = get_openai_client()
    
    # Get current page content for context
    try:
        page_title = await page.title()
        visible_text = await page.inner_text('body')
        # Limit text to avoid token limits
        visible_text = visible_text[:1000] + "..." if len(visible_text) > 1000 else visible_text
    except:
        page_title = "Unknown"
        visible_text = "Unable to read page content"
    
    action_prompt = f"""
        You are a web automation specialist. Given the current context, determine the specific browser action needed for this step.

        Original Task: "{task}"
        Current Step: "{step_description}"
        Current URL: {current_url}
        Page Title: {page_title}
        Visible Page Content: {visible_text[:500]}...

        Respond with ONE of these action types followed by the specific details:

        NAVIGATE: [URL] - Navigate to a specific URL
        FILL: [selector] | [text] - Fill an input field (use CSS selector)
        CLICK: [selector] - Click an element (use CSS selector)
        PRESS: [key] - Press a keyboard key (Enter, Tab, etc.)
        SCROLL: [direction] - Scroll page (down, up)
        WAIT: [seconds] - Wait for a specific time
        EXTRACT: [selector] - Extract text from an element
        SCREENSHOT: - Take a screenshot

        Choose the most appropriate action for this step. Be specific with selectors.
        If unsure about selectors, use common ones like: input[name="q"], button[type="submit"], .search-button, #search, etc.

        Respond with ONLY the action line, nothing else.
        """

    try:
        response = client.chat.completions.create(
            model=manager.get_model_info(alias).id,
            max_tokens=256,
            messages=[{"role": "user", "content": action_prompt}]
        )
        
        action_line = response.choices[0].message.content.strip()
        return action_line
        
    except Exception as e:
        print(f"❌ AI action generation failed: {e}")
        return "WAIT: 2"  # Fallback action

def plan_task_steps(task):
    """Legacy function - now just returns a placeholder. Real planning happens in async version."""
    return [f"AI will analyze and plan steps for: {task}"]

async def execute_ai_generated_step(step_description, page, session_id, screenshot_paths, task):
    """Execute a step using AI-generated actions."""
    print(f"🔄 STEP: {step_description}")
    
    # Take a screenshot before the step
    timestamp = int(time.time())
    screenshot_path = f"screenshots/screenshot_{session_id}_{timestamp}_before_{len(screenshot_paths)}.png"
    try:
        await page.screenshot(path=os.path.join("static", screenshot_path))
        screenshot_paths.append(screenshot_path)
    except:
        pass
    
    # Get AI-generated action for this step
    current_url = page.url
    action_line = await generate_step_action_with_ai(step_description, current_url, task, page)
    print(f"🤖 AI Action: {action_line}")
    
    # Parse and execute the action
    try:
        if action_line.startswith("NAVIGATE:"):
            url = action_line.split("NAVIGATE:", 1)[1].strip()
            await page.goto(url)
            await page.wait_for_load_state('networkidle')
            
        elif action_line.startswith("FILL:"):
            parts = action_line.split("FILL:", 1)[1].strip().split("|")
            if len(parts) >= 2:
                selector = parts[0].strip()
                text = parts[1].strip()
                await page.fill(selector, text)
            
        elif action_line.startswith("CLICK:"):
            selector = action_line.split("CLICK:", 1)[1].strip()
            await page.click(selector, timeout=10000)
            await page.wait_for_load_state('networkidle')
            
        elif action_line.startswith("PRESS:"):
            key = action_line.split("PRESS:", 1)[1].strip()
            await page.keyboard.press(key)
            await page.wait_for_load_state('networkidle')
            
        elif action_line.startswith("SCROLL:"):
            direction = action_line.split("SCROLL:", 1)[1].strip().lower()
            if direction == "down":
                await page.evaluate("window.scrollBy(0, window.innerHeight)")
            elif direction == "up":
                await page.evaluate("window.scrollBy(0, -window.innerHeight)")
                
        elif action_line.startswith("WAIT:"):
            seconds = int(action_line.split("WAIT:", 1)[1].strip())
            await page.wait_for_timeout(seconds * 1000)
            
        elif action_line.startswith("EXTRACT:"):
            selector = action_line.split("EXTRACT:", 1)[1].strip()
            try:
                text = await page.inner_text(selector)
                print(f"📝 Extracted: {text[:100]}...")
            except:
                print("📝 Could not extract text from selector")
                
        elif action_line.startswith("SCREENSHOT:"):
            # Screenshot will be taken below anyway
            await page.wait_for_timeout(1000)
            
        else:
            print(f"⚠️ Unknown action format: {action_line}")
            await page.wait_for_timeout(2000)  # Default wait
            
    except Exception as e:
        print(f"❌ Action failed: {e}")
        await page.wait_for_timeout(2000)  # Wait and continue
    
    # Check for CAPTCHA after action
    captcha_handled = await detect_and_handle_captcha(page, session_id, screenshot_paths)
    if captcha_handled:
        return True  # Signal that CAPTCHA was handled
    
    # Take a screenshot after the step
    await page.wait_for_timeout(2000)
    timestamp = int(time.time())
    screenshot_path = f"screenshots/screenshot_{session_id}_{timestamp}_after_{len(screenshot_paths)}.png"
    try:
        await page.screenshot(path=os.path.join("static", screenshot_path))
        screenshot_paths.append(screenshot_path)
    except:
        pass
    
    print(f"✅ COMPLETED: {step_description}")
    return False  # No CAPTCHA handled

async def run_browser_automation(task):
    """Run browser automation task with AI-generated step-by-step planning and return paths to screenshots."""
    screenshot_paths = []
    
    # Generate AI plan for the task
    print(f"🧠 AI is analyzing the task: {task}")
    steps = await generate_task_plan_with_ai(task)
    
    print(f"📋 AI GENERATED TASK PLAN:")
    for i, step in enumerate(steps, 1):
        print(f"   {i}. {step}")
    print()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        
        # Generate a unique ID for this session's screenshots
        session_id = str(uuid.uuid4())[:8]
        
        try:
            # Parse the task to understand what the user wants
            task_lower = task.lower()
            
            # Execute each AI-generated step
            for i, step in enumerate(steps, 1):
                print(f"\n🎯 Executing Step {i}/{len(steps)}")
                
                captcha_handled = await execute_ai_generated_step(
                    step, page, session_id, screenshot_paths, task
                )
                
                if captcha_handled:
                    print("🛡️ CAPTCHA detected and handled, stopping current task flow")
                    break
                
                # Small delay between steps for stability
                await page.wait_for_timeout(1000)
            
            print("🎯 TASK COMPLETED SUCCESSFULLY!")
            print(f"📸 Total screenshots taken: {len(screenshot_paths)}")
            
        except Exception as e:
            print(f"❌ Error during browser automation: {str(e)}")
        finally:
            await browser.close()
    
    return screenshot_paths

async def detect_and_handle_captcha(page, session_id, screenshot_paths):
    """Detect CAPTCHA and navigate to another URL or handle it."""
    try:
        # Multiple CAPTCHA detection patterns
        captcha_selectors = [
            'div.captcha',
            '[class*="captcha"]',
            '[id*="captcha"]',
            'iframe[src*="recaptcha"]',
            '.g-recaptcha',
            '[class*="hcaptcha"]',
            '.cf-browser-verification',
            '[data-testid*="captcha"]',
            'img[alt*="captcha"]',
            'img[src*="captcha"]'
        ]
        
        captcha_detected = False
        for selector in captcha_selectors:
            element = await page.query_selector(selector)
            if element:
                print(f"CAPTCHA detected with selector: {selector}")
                captcha_detected = True
                break
        
        # Also check for CAPTCHA-related text on the page
        page_text = await page.inner_text('body')
        captcha_keywords = ['captcha', 'verification', 'prove you are human', 'security check', 'robot check']
        for keyword in captcha_keywords:
            if keyword.lower() in page_text.lower():
                print(f"CAPTCHA detected by keyword: {keyword}")
                captcha_detected = True
                break
        
        if captcha_detected:
            print("CAPTCHA detected! Taking screenshot and navigating elsewhere...")
            
            # Take a screenshot of the CAPTCHA page
            timestamp = int(time.time())
            screenshot_path = f"screenshots/screenshot_{session_id}_{timestamp}_captcha.png"
            await page.screenshot(path=os.path.join("static", screenshot_path))
            screenshot_paths.append(screenshot_path)
            
            # Navigate to an alternative URL (you can customize this)
            alternative_urls = [
                "https://www.bing.com",
                "https://duckduckgo.com",
                "https://www.yahoo.com",
                "https://www.startpage.com",
                "https://searx.be"
            ]
            
            # Choose an alternative URL
            alternative_url = alternative_urls[0]  # You can randomize this
            print(f"Navigating to alternative URL: {alternative_url}")
            await page.goto(alternative_url)
            await page.wait_for_load_state('networkidle')
            
            # Take a screenshot of the alternative page
            timestamp = int(time.time())
            screenshot_path = f"screenshots/screenshot_{session_id}_{timestamp}_alternative.png"
            await page.screenshot(path=os.path.join("static", screenshot_path))
            screenshot_paths.append(screenshot_path)
            
            return True  # CAPTCHA was detected and handled
        else:
            print("No CAPTCHA detected. Proceeding with normal flow.")
            return False  # No CAPTCHA detected
            
    except Exception as e:
        print(f"Error while checking for CAPTCHA: {e}")
        return False

if __name__ == '__main__':
    app.run(debug=True)
