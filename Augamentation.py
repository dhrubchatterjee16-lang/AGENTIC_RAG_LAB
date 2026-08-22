import os
from google import genai
from google.colab import userdata

# Get Gemini API key from Colab Secrets (or prompt if not set)
# To set secret in Colab: Click Key icon on left sidebar -> Add secret name "GEMINI_API_KEY"
try:
    api_key = userdata.get('GEMINI_API_KEY')
except:
    api_key = input("Enter your Gemini API Key: ")

client = genai.Client(api_key=api_key)

def generate_rag_answer(query: str, top_k: int = 2) -> str:
    # Step 1: Retrieve relevant context chunks
    context_chunks = retrieve_relevant_context(query, top_k=top_k)
    context_text = "\n\n".join(context_chunks)
    
    # Step 2: Build the Augmented Prompt
    augmented_prompt = f"""You are a helpful AI assistant. Answer the question using ONLY the provided context below.
If the context does not contain enough information to answer, state "I cannot find the answer in the provided documents."

CONTEXT:
---------------------
{context_text}
---------------------

USER QUESTION: {query}

ANSWER:"""

    # Step 3: Call LLM
    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=augmented_prompt
    )
    
    return response.text, context_chunks
