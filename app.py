from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "✅ Brutus chatbot kjører!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "")

    if "naprapat" in question.lower():
        return jsonify({"answer": "En naprapat hos STERK jobber med muskel- og leddplager."})
    
    return jsonify({"answer": "Beklager, jeg har ikke et svar på det enda."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)



