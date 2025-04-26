from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Tillater forespørsler fra WordPress og andre domener

# Helse-sjekk
@app.route("/")
def home():
    return "✅ Brutus chatbot kjører!"

# Chat-endepunkt
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "")

    # Midlertidig enkel logikk
    if "naprapat" in question.lower():
        return jsonify({"answer": "En naprapat hos STERK hjelper med muskel- og leddplager."})
    elif "fysioterapeut" in question.lower():
        return jsonify({"answer": "En fysioterapeut hos STERK hjelper deg med rehabilitering og smertebehandling."})
    elif "osteopat" in question.lower():
        return jsonify({"answer": "En osteopat hos STERK behandler muskel- og skjelettplager helhetlig."})
    else:
        return jsonify({"answer": "Beklager, jeg har ikke et godt svar på det enda."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


