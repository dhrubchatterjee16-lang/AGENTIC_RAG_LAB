from google import genai
from google.colab import userdata

try:
    api_key = userdata.get('GEMINI_API_KEY')
except:
    api_key = input("Enter your Gemini API Key: ")

client = genai.Client(api_key=api_key)

def intermediate_rag_pipeline(query: str) -> str:
    # Step 1: Hybrid Search (Retrieve candidate pool of 6)
    candidates = hybrid_search(query, top_n=6)
    
    # Step 2: Cross-Encoder Re-ranking (Filter down to top 2 highest precision)
    top_context = rerank_documents(query, candidates, top_k=2)
    
    formatted_context = "\n\n".join(top_context)
    
    # Step 3: Generate with Gemini
    prompt = f"""You are an expert technical assistant. Answer the user prompt accurately based ONLY on the context below.

CONTEXT:
{formatted_context}

QUESTION: {query}

Provide a concise answer with relevant Part IDs or numerical details if available."""

    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt
    )
    
    return response.text, top_context

# Test Query
test_query = "What is the part ID for the Sunshield Replacement and what temperature does it maintain?"
answer, retrieved_ctx = intermediate_rag_pipeline(test_query)

print("=== INTERMEDIATE RAG RESULT ===")
print(f"Query: {test_query}\n")
print(f"Answer:\n{answer}")
