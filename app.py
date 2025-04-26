from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import numpy as np
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Konfig
openai.api_key = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)
CORS(app)

# Healthcheck
@app.route("/")
def home():
    return "✅ Brutus chatbot kjører!"

# Hjelpefunksjon: cosine similarity
def cosine_similarity(a, b):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Embedding
def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

# Hent relevante svar
def fetch_relevant_chunks(query_embedding, top_k=1):
    response = supabase.table("sterk_chatbot_trening").select("*").execute()
    records = response.data

    results = []
    for record in records:
        db_embedding = eval(record["embedding"])
        similarity = cosine_similarity(query_embedding, db_embedding)
        results.append((similarity, record))

    # Sorter etter relevans
    sorted_results = sorted(results, key=lambda x: x[0], reverse=True)
    top_results = [r[1] for r in sorted_results[:top_k]]
    return top_results

# Chat-endepunkt
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    question = data.get("question", "")

    try:
        query_embedding = get_embedding(question)
        relevant = fetch_relevant_chunks(query_embedding)

        if relevant:
            return jsonify({"answer": relevant[0]["content"]})
        else:
            return jsonify({"answer": "Beklager, jeg fant ingen relevant informasjon."})
    except Exception as e:
        print("Feil:", e)
        return jsonify({"answer": "Beklager, det oppstod en teknisk feil."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)




