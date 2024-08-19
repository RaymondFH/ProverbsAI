import os
from flask import Flask, render_template, request, jsonify
import anthropic

app = Flask(__name__)

# Initialize the Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        problem = request.form['problem']
        
        # Call Claude API
        response = client.completions.create(
            model="claude-3-sonnet-20240229",
            max_tokens_to_sample=300,
            prompt=f"Given the following personal problem: '{problem}', provide a relevant Bible verse, gospel passage, or other section from Catholic teachings that addresses this situation. Include the verse reference and a brief explanation of how it relates to the problem."
        )
        
        return jsonify({'response': response.completion})
    
    return render_template('index.html')

if __name__ == '__main__':
    # Use the PORT environment variable provided by Render, or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)