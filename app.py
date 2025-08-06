from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "API up"})

# Inicializar cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "")

        if not prompt:
            return jsonify({"error": "No se envió ninguna pregunta"}), 400

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente esotérico experto en tarot, litomancia y astrología."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )

        result = response.choices[0].message.content.strip()
        return jsonify({"response": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
# Interfaz de chat estático en /chat
@app.route("/chat", methods=["GET"])
def chat_ui():
    return \"\"\"
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8"/>
      <title>Chat Esotérico</title>
      <style>
        body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; padding: 2rem; }
        #messages { width: 100%; max-width: 400px; height: 300px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; margin-bottom: 1rem; }
        .user { text-align: right; margin: 5px; }
        .bot  { text-align: left; margin: 5px; }
        #user-input { width: 75%; padding: 0.5rem; }
        #send-btn  { padding: 0.5rem 1rem; }
      </style>
    </head>
    <body>
      <h1>Chat Esotérico</h1>
      <div id="messages"></div>
      <div>
        <input id="user-input" placeholder="Escribe tu consulta…"/>
        <button id="send-btn">Enviar</button>
      </div>
      <script>
        const API_URL = "/api/chat";
        const messagesEl = document.getElementById("messages");
        document.getElementById("send-btn").onclick = async () => {
          const text = document.getElementById("user-input").value.trim();
          if (!text) return;
          const u = document.createElement("div"); u.textContent = text; u.className = "user"; messagesEl.append(u);
          document.getElementById("user-input").value = "";
          const res = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt: text })
          });
          const data = await res.json();
          const b = document.createElement("div"); b.textContent = data.response || data.error; b.className = "bot"; messagesEl.append(b);
          messagesEl.scrollTop = messagesEl.scrollHeight;
        };
      </script>
    </body>
    </html>
    \"\"\"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


