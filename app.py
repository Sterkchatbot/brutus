from flask import Flask, request, jsonify

app = Flask(__name__)

# Helse-sjekk
@app.route("/", methods=["GET"])
def home():
    return "✅ Brutus chatbot kjører!"

# Chat-endepunkt
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"answer": "Beklager, jeg mottok ikke spørsmålet ditt."})

    # Midlertidig dummy-svar
    if "naprapat" in question.lower():
        return jsonify({"answer": "En naprapat hos STERK jobber med muskel- og leddplager."})
    
    return jsonify({"answer": "Beklager, jeg har ikke et svar på det ennå."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


