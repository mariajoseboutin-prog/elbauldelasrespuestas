from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise EnvironmentError("La variable de entorno OPENAI_API_KEY no está definida.")
openai.api_key = openai_api_key

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return '✅ API con IA funcionando en Flask'

@app.route('/api/chat', methods=['POST'])
def chat():
    if not request.is_json:
        return jsonify({'error': 'El cuerpo de la petición debe ser JSON'}), 400

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'error': 'No se pudo interpretar el JSON'}), 400

    prompt = data.get('prompt', '')
    if not prompt or not prompt.strip():
        return jsonify({'error': 'No se envió ningún prompt'}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=200
        )
        result = response['choices'][0]['message']['content']
        return jsonify({'respuesta': result})
    except openai.error.AuthenticationError:
        return jsonify({'error': 'Error de autenticación con OpenAI'}), 401
    except openai.error.OpenAIError as oe:
        return jsonify({'error': f'Error con la API de OpenAI: {str(oe)}'}), 502
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

if __name__ == '__main__':
    app.run()