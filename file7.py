# 1. Install & Imports
!pip install -q chromadb sentence-transformers google-genai ddgs

import json
import re
import chromadb
from chromadb.utils import embedding_functions
from google import genai
from google.colab import userdata
from ddgs import DDGS

# 2. API Key Setup
try:
    api_key = userdata.get('GEMINI_API_KEY')
except:
    api_key = input("Enter your Gemini API Key: ")

client = genai.Client(api_key=api_key)

# 3. Vector DB Setup
chroma_client = chromadb.Client()
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
vector_store = chroma_client.get_or_create_collection("crag_print_db", embedding_function=embedding_fn)

tech_docs = [
    "NovaEngine v4.0 is a proprietary database indexing tool developed by QuantumLabs.",
    "NovaEngine v4.0 utilizes a B-Tree + LSM-Tree hybrid architecture to achieve 100,000 writes per second.",
    "NovaEngine v4.0 requires at least 16GB of RAM and NVMe storage for optimal performance."
]

vector_store.add(documents=tech_docs, ids=[f"doc_{i}" for i in range(len(tech_docs))])

# 4. Helper Functions
def crag_evaluator(query, docs):
    if not docs:
        return "INCORRECT", 0.0
    prompt = f"""Evaluate context quality for query.
Score > 0.7 -> 'CORRECT'
Score 0.3-0.7 -> 'AMBIGUOUS'
Score < 0.3 -> 'INCORRECT'

Return JSON ONLY: {{"score": 0.85, "action": "CORRECT"}}

QUERY: {query}
CONTEXT: {" ".join(docs)}"""

    res = client.models.generate_content(model='gemini-3.6-flash', contents=prompt)
    try:
        clean = res.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean)
        return data.get("action", "INCORRECT").upper(), float(data.get("score", 0.0))
    except:
        return "INCORRECT", 0.0

def web_search(query):
    results_text = ""
    try:
        with DDGS() as ddgs:
            for r in list(ddgs.text(query, max_results=2)):
                results_text += f"{r['title']}: {r['body']}\n"
    except Exception as e:
        results_text = "Web search fallback data."
    return results_text

def run_crag(query):
    print("\n" + "="*70)
    print(f"🔍 USER QUERY: '{query}'")
    print("="*70)

    # Retrieval
    vector_res = vector_store.query(query_texts=[query], n_results=2)['documents'][0]
    print(f"📥 Step 1: Retrieved from Vector DB -> {vector_res}")

    # CRAG Evaluator
    action, score = crag_evaluator(query, vector_res)
    print(f"📊 Step 2: CRAG Evaluator Decision -> Action Path: [{action}] (Confidence Score: {score})")

    # Execution Paths
    if action == "CORRECT":
        print("🟢 Step 3: Action Path [CORRECT] -> Using internal Vector DB context directly.")
        context = "\n".join(vector_res)
    elif action == "AMBIGUOUS":
        print("🟡 Step 3: Action Path [AMBIGUOUS] -> Fetching Web Search to supplement Vector DB...")
        web_res = web_search(query)
        context = "Vector Docs:\n" + "\n".join(vector_res) + "\n\nWeb Search:\n" + web_res
    else:
        print("🔴 Step 3: Action Path [INCORRECT] -> Discarding Vector DB! Relying 100% on Web Search...")
        web_res = web_search(query)
        context = web_res

    # Gemini Generation
    gen_prompt = f"Answer the query strictly based on context.\nCONTEXT:\n{context}\n\nQUERY: {query}"
    answer = client.models.generate_content(model='gemini-3.6-flash', contents=gen_prompt).text

    print("\n💡 FINAL GENERATED ANSWER:")
    print(answer)
    print("-" * 70)

# =========================================================
# RUNNING ALL 3 TEST SCENARIOS
# =========================================================

# Test 1: Vector DB Has Answer (CORRECT)
run_crag("What write throughput can NovaEngine v4.0 achieve?")

# Test 2: Vector DB Lacks Answer (INCORRECT -> Web Search Fallback)
run_crag("What is the capital of France?")

# Test 3: Partial Vector DB Answer (AMBIGUOUS -> Combined)
run_crag("How fast is NovaEngine v4.0 compared to MySQL?")
