from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Gjør at WordPress får lov å sende spørringer hit

# Helse-sjekk endepunkt
@app.route("/")
def home():
    return "✅ Brutus chatbot kjører!"

# Chat-endepunkt som mottar spørsmål fra brukeren
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        question = data.get("question", "")

        # Midlertidig enkel svarlogikk
        if "naprapat" in question.lower():
            return jsonify({"answer": "En naprapat hos STERK jobber med muskel- og leddplager, og hjelper med behandling av nakke, rygg og ledd."})
        elif "fysioterapeut" in question.lower():
            return jsonify({"answer": "En fysioterapeut hos STERK hjelper deg med rehabilitering etter skade eller operasjon, og jobber med muskel- og skjelettplager."})
        else:
            return jsonify({"answer": "Beklager, jeg har ikke et svar på det enda. Kan du prøve å omformulere spørsmålet?"})
    
    except Exception as e:
        return jsonify({"answer": f"Beklager, det oppstod en feil: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

