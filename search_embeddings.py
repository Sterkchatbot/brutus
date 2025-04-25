import os
import ast
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI
from supabase import create_client

# Last inn miljøvariabler
load_dotenv()

# Koble til OpenAI og Supabase
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def get_embedding(text):
    response = openai_client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def fetch_relevant_chunks(query_embedding, top_k=3):
    response = supabase.table("sterk_chatbot_trening").select("*").execute()
    all_chunks = response.data

    scored = []
    for row in all_chunks:
        embedding_raw = row.get("embedding")
        if not embedding_raw:
            continue
        # Hvis embedding er lagret som tekst, konverter til liste
        if isinstance(embedding_raw, str):
            embedding = ast.literal_eval(embedding_raw)
        else:
            embedding = embedding_raw

        similarity = cosine_similarity(query_embedding, embedding)
        scored.append((similarity, row))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = [row for score, row in scored[:top_k]]

    return top

def generate_answer(question, context_chunks):
    context_texts = "\n\n".join(f"- {chunk['content']}" for chunk in context_chunks)

    system_prompt = (
        "Du er en hjelpsom og hyggelig chatbot for STERK Helse. "
        "Svar kort og tydelig basert på informasjonen under. "
        "Hvis spørsmålet handler om behandling, anbefal en time på https://www.sterkhelse.no/behandlere/"
    )

    user_prompt = f"""
Kontekst:
{context_texts}

Spørsmål: {question}
"""

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    bruker_spm = input("Hva vil du spørre chatboten om? ➤ ")
    emb = get_embedding(bruker_spm)
    relevante_chunks = fetch_relevant_chunks(emb)
    svar = generate_answer(bruker_spm, relevante_chunks)
    print("\n🤖 Chatbot svarer:\n", svar)
