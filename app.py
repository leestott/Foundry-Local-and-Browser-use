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

async def run_browser_automation(task):
    """Run browser automation task and return paths to screenshots."""
    screenshot_paths = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        
        # Generate a unique ID for this session's screenshots
        session_id = str(uuid.uuid4())[:8]
        
        try:
            # Parse the task to understand what the user wants
            task_lower = task.lower()
            
            # Handle different types of navigation tasks
            if "google" in task_lower:
                await page.goto("https://www.google.com")
                search_term = task_lower.replace("google", "").replace("search for", "").replace("search", "").strip()
                if search_term:
                    await page.fill('input[name="q"]', search_term)
                    await page.press('input[name="q"]', 'Enter')
                    await page.wait_for_load_state('networkidle')
                    
                    # Take a screenshot of the search results
                    timestamp = int(time.time())
                    screenshot_path = f"screenshots/screenshot_{session_id}_{timestamp}.png"
                    await page.screenshot(path=os.path.join("static", screenshot_path))
                    screenshot_paths.append(screenshot_path)
                    
                    # Click on the first search result
                    try:
                        await page.click('div.g a', timeout=5000)
                        await page.wait_for_load_state('networkidle')
                        
                        # Take a screenshot of the page
                        timestamp = int(time.time())
                        screenshot_path = f"screenshots/screenshot_{session_id}_{timestamp}.png"
                        await page.screenshot(path=os.path.join("static", screenshot_path))
                        screenshot_paths.append(screenshot_path)
                    except:
                        pass  # If clicking the first result fails, just continue
            
            elif "reddit" in task_lower:
                await page.goto("https://www.reddit.com")
                search_term = task_lower.replace("reddit", "").replace("search for", "").replace("search", "").strip()
                if search_term:
                    # Take a screenshot of Reddit homepage
                    timestamp = int(time.time())
                    screenshot_path = f"screenshots/screenshot_{session_id}_{timestamp}.png"
                    await page.screenshot(path=os.path.join("static", screenshot_path))
                    screenshot_paths.append(screenshot_path)
                    
                    # Search for the term
                    try:
                        await page.click('button[aria-label="Search"]', timeout=5000)
                        await page.fill('input[type="search"]', search_term)
                        await page.press('input[type="search"]', 'Enter')
                        await page.wait_for_load_state('networkidle')
                        
                        # Take a screenshot of the search results
                        timestamp = int(time.time())
                        screenshot_path = f"screenshots/screenshot_{session_id}_{timestamp}.png"
                        await page.screenshot(path=os.path.join("static", screenshot_path))
                        screenshot_paths.append(screenshot_path)
                        
                        # Click on the first post if available
                        try:
                            await page.click('div[data-testid="post-container"]', timeout=5000)
                            await page.wait_for_load_state('networkidle')
                            
                            # Take a screenshot of the post
                            timestamp = int(time.time())
                            screenshot_path = f"screenshots/screenshot_{session_id}_{timestamp}.png"
                            await page.screenshot(path=os.path.join("static", screenshot_path))
                            screenshot_paths.append(screenshot_path)
                        except:
                            pass  # If clicking the post fails, just continue
                    except:
                        pass  # If search fails, just continue
            
            elif "amazon" in task_lower or "product" in task_lower or "shopping" in task_lower:
                # Extract search terms for shopping
                search_term = task_lower
                for term in ["amazon", "product", "shopping", "search for", "search", "for", "on"]:
                    search_term = search_term.replace(term, "")
                search_term = search_term.strip()
                
                # Navigate to Amazon and search
                await page.goto("https://www.amazon.com")
                
                # Take a screenshot of Amazon homepage
                timestamp = int(time.time())
                screenshot_path = f"screenshots/screenshot_{session_id}_{timestamp}.png"
                await page.screenshot(path=os.path.join("static", screenshot_path))
                screenshot_paths.append(screenshot_path)
                
                if search_term:
                    try:
                        await page.fill('input#twotabsearchtextbox', search_term)
                        await page.press('input#twotabsearchtextbox', 'Enter')
                        await page.wait_for_load_state('networkidle')
                        
                        # Take a screenshot of the search results
                        timestamp = int(time.time())
                        screenshot_path = f"screenshots/screenshot_{session_id}_{timestamp}.png"
                        await page.screenshot(path=os.path.join("static", screenshot_path))
                        screenshot_paths.append(screenshot_path)
                        
                        # Click on first product
                        try:
                            await page.click('div[data-component-type="s-search-result"] h2 a', timeout=5000)
                            await page.wait_for_load_state('networkidle')
                            
                            # Take a screenshot of the product page
                            timestamp = int(time.time())
                            screenshot_path = f"screenshots/screenshot_{session_id}_{timestamp}.png"
                            await page.screenshot(path=os.path.join("static", screenshot_path))
                            screenshot_paths.append(screenshot_path)
                        except:
                            pass  # If clicking the product fails, just continue
                    except:
                        pass  # If search fails, just continue
            
            elif "wikipedia" in task_lower or "information" in task_lower or "about" in task_lower:
                # Extract search terms for information
                search_term = task_lower
                for term in ["wikipedia", "information", "about", "search for", "search", "for", "on"]:
                    search_term = search_term.replace(term, "")
                search_term = search_term.strip()
                
                # Navigate to Wikipedia and search
                await page.goto("https://www.wikipedia.org")
                
                # Take a screenshot of Wikipedia homepage
                timestamp = int(time.time())
                screenshot_path = f"screenshots/screenshot_{session_id}_{timestamp}.png"
                await page.screenshot(path=os.path.join("static", screenshot_path))
                screenshot_paths.append(screenshot_path)
                
                if search_term:
                    try:
                        await page.fill('input#searchInput', search_term)
                        await page.press('input#searchInput', 'Enter')
                        await page.wait_for_load_state('networkidle')
                        
                        # Take a screenshot of the article
                        timestamp = int(time.time())
                        screenshot_path = f"screenshots/screenshot_{session_id}_{timestamp}.png"
                        await page.screenshot(path=os.path.join("static", screenshot_path))
                        screenshot_paths.append(screenshot_path)
                        
                        # Scroll down to get more content
                        await page.evaluate("window.scrollBy(0, window.innerHeight)")
                        await page.wait_for_timeout(1000)
                        
                        # Take another screenshot after scrolling
                        timestamp = int(time.time())
                        screenshot_path = f"screenshots/screenshot_{session_id}_{timestamp}.png"
                        await page.screenshot(path=os.path.join("static", screenshot_path))
                        screenshot_paths.append(screenshot_path)
                    except:
                        pass  # If search fails, just continue
            
            else:
                # Default to navigating to the URL or search term on Google
                if task.startswith(("http://", "https://")):
                    await page.goto(task)
                    await page.wait_for_load_state('networkidle')
                else:
                    await page.goto(f"https://www.google.com/search?q={task}")
                    await page.wait_for_load_state('networkidle')
                
                # Take a screenshot of the page
                timestamp = int(time.time())
                screenshot_path = f"screenshots/screenshot_{session_id}_{timestamp}.png"
                await page.screenshot(path=os.path.join("static", screenshot_path))
                screenshot_paths.append(screenshot_path)
                
                # Scroll down to get more content
                await page.evaluate("window.scrollBy(0, window.innerHeight)")
                await page.wait_for_timeout(1000)
                
                # Take another screenshot after scrolling
                timestamp = int(time.time())
                screenshot_path = f"screenshots/screenshot_{session_id}_{timestamp}.png"
                await page.screenshot(path=os.path.join("static", screenshot_path))
                screenshot_paths.append(screenshot_path)
                
                # If on Google search results, click on the first result
                if "google.com/search" in page.url:
                    try:
                        await page.click('div.g a', timeout=5000)
                        await page.wait_for_load_state('networkidle')
                        
                        # Take a screenshot of the page
                        timestamp = int(time.time())
                        screenshot_path = f"screenshots/screenshot_{session_id}_{timestamp}.png"
                        await page.screenshot(path=os.path.join("static", screenshot_path))
                        screenshot_paths.append(screenshot_path)
                    except:
                        pass  # If clicking fails, just continue
            
        except Exception as e:
            print(f"Error during browser automation: {str(e)}")
        finally:
            await browser.close()
    
    return screenshot_paths

if __name__ == '__main__':
    app.run(debug=True)
