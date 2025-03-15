from flask import Flask, request, jsonify
from flask_cors import CORS
import bot_no_gui as bot
import os

app = Flask(__name__)
CORS(app)  # Allows all origins

@app.route('/')
def index():
    return "this works"

@app.route("/app", methods=["POST"])
def handle_request():
    data = request.get_json()

    # Check if it's a database initialization request
    if "url" in data:
        url = data.get("url")
        bot.create_database(url)
        return jsonify({"success": True, "message": "Database initialized successfully"})

    # Otherwise, handle the chat request
    elif "message" in data:
        user_input = data.get("message")
        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        # Pass the user's input to your bot
        response = bot.run(user_input)
        return jsonify({"response": response})

    return jsonify({"error": "Invalid request"}), 400

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))  # Get Render's assigned port
    app.run(host='0.0.0.0', port=port)   # Listen on all interfaces
