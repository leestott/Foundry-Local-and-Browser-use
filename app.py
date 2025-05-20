import os
from flask import Flask, render_template, request, jsonify
import openai
from foundry_local import FoundryLocalManager

app = Flask(__name__)



@app.route('/')
def index():
    """Render the home page with the chat interface."""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Generate a response from the AI model."""
    alias = "phi-3.5-mini"  # Default model alias

    # Initialize the FoundryLocalManager globally
    manager = FoundryLocalManager(alias)
    

    # Get user prompt
    data = request.json
    user_prompt = data.get('prompt', '')
        
    if not user_prompt:
        return jsonify({"error": "No prompt provided"}), 400
            
    # Connect OpenAI client to the local Foundry endpoint
    client = openai.OpenAI(
        base_url=manager.endpoint,
        api_key=manager.api_key  # Not required for local usage
    )

    # Generate a response from the local model
    response = client.chat.completions.create(
            model=manager.get_model_info(alias).id,
            max_tokens=4096,
            messages=[{"role": "user", "content": user_prompt}]
    )
        
    # Extract and return the response content
    response_content = response.choices[0].message.content
    return jsonify({"response": response_content})
        

if __name__ == '__main__':
    app.run(debug=True)
