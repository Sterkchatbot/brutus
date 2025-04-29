from flask import Flask, request, jsonify
from flask_cors import CORS
from search_embeddings import fetch_relevant
import os  # ← denne manglet

app = Flask(__name__)
CORS(app)

@app.route("/")
def health_check():
    return "✅ STERK Chatbot kjører!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"error": "Ingen spørsmål sendt."}), 400

    # Hent topp-tre med override
    results = fetch_relevant(question, top_k=1)
    score, content, url = results[0]

    return jsonify({
        "answer": content,
        "source": url,
        "confidence": round(score, 2)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))




