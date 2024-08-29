import os
from flask import Flask, render_template, request, jsonify
from anthropic import Anthropic

# Import the BibleLinkGenerator
from bible_link_generator import BibleLinkGenerator

app = Flask(__name__)

# Initialize the Anthropic client
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Initialize the BibleLinkGenerator
link_generator = BibleLinkGenerator()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        problem = request.form['problem']
        
        # Call Claude API using the Messages API
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=300,
            messages=[
                {
                    "role": "user",
                    "content": f"Given the following personal problem: '{problem}', provide a relevant Bible verse, gospel passage, or other section from Catholic teachings that addresses this situation. Include the verse reference and a brief explanation of how it relates to the problem."
                }
            ]
        )
        
        # Extract the response content
        response_content = message.content[0].text
        
        # Generate Bible links
        bible_links = link_generator.process_ai_response(response_content)
        
        return jsonify({
            'response': response_content,
            'bible_links': bible_links
        })
    
    return render_template('index.html')

if __name__ == '__main__':
    # Use the PORT environment variable provided by Render, or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)