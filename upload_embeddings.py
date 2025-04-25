import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
print("SUPABASE_URL =", url)
print("SUPABASE_KEY =", key[:6] + "...")

supabase = create_client(url, key)

data = {
    "slug": "test_slug",
    "content": "Dette er testinnhold for STERK chatbot.",
    "URL": "https://eksempel.no",
    "embedding": [0.0] * 1536  # Dummy vector
}

try:
    result = supabase.table("sterk_chatbot_trening").insert(data).execute()
    print("✅ Lagt til:", result)
except Exception as e:
    print("❌ Feil ved innsending:")
    import traceback
    traceback.print_exc()




