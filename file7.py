import os
from google import genai
from google.colab import userdata

# Get Gemini API key
try:
    api_key = userdata.get('GEMINI_API_KEY')
except:
    api_key = input("Enter your Gemini API Key: ")

client = genai.Client(api_key=api_key)

# Setup ChromaDB for local vector retrieval
import chromadb
from chromadb.utils import embedding_functions

chroma_client = chromadb.Client()
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
vector_collection = chroma_client.get_or_create_collection("agentic_kb", embedding_function=embedding_fn)

# Ingest sample company policy documents
sample_docs = [
    "Acme Corp Remote Work Policy: Employees are eligible for $500 home office stipend after 90 days of employment.",
    "Acme Corp Leave Policy: Full-time employees receive 15 days of paid time off (PTO) annually.",
    "Acme Corp Security Protocol: All employee devices must use 2-Factor Authentication via Okta."
]

vector_collection.add(
    documents=sample_docs,
    ids=[f"id_{i}" for i in range(len(sample_docs))]
)

print(f"Indexed {vector_collection.count()} internal documents into ChromaDB!")
