import chromadb
from chromadb.utils import embedding_functions

# 1. Initialize an in-memory ChromaDB client
chroma_client = chromadb.Client()

# 2. Use a free, lightweight embedding model from SentenceTransformers (all-MiniLM-L6-v2)
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# 3. Create or get a vector collection
collection = chroma_client.get_or_create_collection(
    name="knowledge_base",
    embedding_function=embedding_fn
)

# 4. Insert chunks into ChromaDB with unique IDs
ids = [f"doc_chunk_{i}" for i in range(len(chunks))]
collection.add(
    documents=chunks,
    ids=ids
)

print(f"Successfully stored {collection.count()} chunks in ChromaDB!")
