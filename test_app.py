#!/usr/bin/env python3
"""
Demo script to test the Foundry Local AI Chat with Screenshot functionality
"""

import requests

def test_foundry_local_app():
    """Test the main endpoints of the Foundry Local application."""
    base_url = "http://127.0.0.1:5000"
    
    print("🧪 Testing Foundry Local AI Chat with Screenshots")
    print("=" * 50)
    
    # Test 1: Check status
    print("1. Testing status endpoint...")
    try:
        response = requests.get(f"{base_url}/status")
        if response.status_code == 200:
            status_data = response.json()
            print(f"   ✅ Status: {status_data.get('status')}")
            print(f"   📁 Model: {status_data.get('model')}")
        else:
            print(f"   ❌ Status check failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Status check error: {e}")
    
    print()
    
    # Test 2: Test AI generation
    print("2. Testing AI generation...")
    try:
        response = requests.post(f"{base_url}/generate", 
                               json={"prompt": "What is artificial intelligence?"})
        if response.status_code == 200:
            gen_data = response.json()
            if gen_data.get('success'):
                print(f"   ✅ AI Response generated (length: {len(gen_data.get('response', ''))} chars)")
                print(f"   💬 Preview: {gen_data.get('response', '')[:100]}...")
            else:
                print(f"   ❌ AI generation failed: {gen_data.get('error')}")
        else:
            print(f"   ❌ AI generation failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ AI generation error: {e}")
    
    print()
    
    # Test 3: Test browser automation with screenshots
    print("3. Testing browser automation with screenshots...")
    try:
        response = requests.post(f"{base_url}/automate", 
                               json={"browserTask": "Search for Python programming tutorials"})
        if response.status_code == 200:
            auto_data = response.json()
            if auto_data.get('success'):
                print(f"   ✅ Automation completed")
                print(f"   📋 Plan generated: {len(auto_data.get('plan', ''))} chars")
                screenshots = auto_data.get('screenshots', [])
                print(f"   📸 Screenshots generated: {len(screenshots)}")
                for i, screenshot in enumerate(screenshots):
                    print(f"      - Step {i+1}: {screenshot.get('description')}")
            else:
                print(f"   ❌ Automation failed: {auto_data.get('error')}")
        else:
            print(f"   ❌ Automation failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Automation error: {e}")
    
    print()
    
    # Test 4: List screenshots
    print("4. Testing screenshot listing...")
    try:
        response = requests.get(f"{base_url}/list-screenshots")
        if response.status_code == 200:
            screenshots_data = response.json()
            if screenshots_data.get('success'):
                count = screenshots_data.get('count', 0)
                print(f"   ✅ Listed {count} screenshots")
                if count > 0:
                    for screenshot in screenshots_data.get('screenshots', [])[:3]:
                        print(f"      - {screenshot.get('filename')} ({screenshot.get('description', 'No description')})")
            else:
                print(f"   ❌ Screenshot listing failed: {screenshots_data.get('error')}")
        else:
            print(f"   ❌ Screenshot listing failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Screenshot listing error: {e}")
    
    print()
    
    # Test 5: Get demo tasks
    print("5. Testing demo tasks...")
    try:
        response = requests.get(f"{base_url}/demo-tasks")
        if response.status_code == 200:
            tasks_data = response.json()
            if tasks_data.get('success'):
                tasks = tasks_data.get('tasks', [])
                print(f"   ✅ {len(tasks)} demo tasks available")
                for task in tasks[:3]:
                    print(f"      - {task}")
            else:
                print(f"   ❌ Demo tasks failed: {tasks_data.get('error')}")
        else:
            print(f"   ❌ Demo tasks failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Demo tasks error: {e}")
    
    print()
    print("🎉 Testing completed!")
    print(f"🌐 Visit {base_url} to try the web interface")

if __name__ == "__main__":
    print("⚠️  Make sure the Flask app is running first!")
    print("   Run: python app.py")
    print()
    
    input("Press Enter to start testing...")
    test_foundry_local_app()
