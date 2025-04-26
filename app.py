from flask import Flask, request, jsonify

app = Flask(__name__)

# Helse-sjekk
@app.route("/")
def home():
    return "✅ Brutus chatbot kjører!"

# En test-endepunkt du kan utvide
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    question = data.get("question", "")

    # Midlertidig svarlogikk – her kan du koble inn søk/embedding senere
    if "naprapat" in question.lower():
        return jsonify({"answer": "En naprapat hos STERK jobber med muskel- og leddplager."})
    
    return jsonify({"answer": "Beklager, jeg har ikke et svar på det enda."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
