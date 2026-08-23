import json
import re
import chromadb
from chromadb.utils import embedding_functions
from google import genai
from google.colab import userdata
from duckduckgo_search import DDGS

# 1. Initialize Gemini Client
try:
    api_key = userdata.get('GEMINI_API_KEY')
except:
    api_key = input("Enter your Gemini API Key: ")

client = genai.Client(api_key=api_key)

# 2. Setup Vector DB
chroma_client = chromadb.Client()
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
vector_store = chroma_client.get_or_create_collection("crag_standalone_db", embedding_function=embedding_fn)

# Internal Tech Docs
tech_docs = [
    "NovaEngine v4.0 is a proprietary database indexing tool developed by QuantumLabs.",
    "NovaEngine v4.0 utilizes a B-Tree + LSM-Tree hybrid architecture to achieve 100,000 writes per second.",
    "NovaEngine v4.0 requires at least 16GB of RAM and NVMe storage for optimal performance.",
    "QuantumLabs default admin port for NovaEngine is 8443."
]

vector_store.add(
    documents=tech_docs,
    ids=[f"doc_{i}" for i in range(len(tech_docs))]
)

print(f"Loaded {vector_store.count()} documents into ChromaDB Vector Store!")
