import os
from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # o "gpt-4" si tienes acceso
            prompt=prompt,
            max_tokens=500,
            temperature=0.7,
        )
        return jsonify({"response": response.choices[0].text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
