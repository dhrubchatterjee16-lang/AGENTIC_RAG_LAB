import chromadb
from chromadb.utils import embedding_functions
from rank_bm25 import BM25Okapi

# 1. Initialize Vector Collection (Dense)
chroma_client = chromadb.Client()
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
vector_collection = chroma_client.get_or_create_collection("hybrid_kb", embedding_function=embedding_fn)

# Add chunks to Vector DB
vector_collection.add(
    documents=[c["text"] for c in processed_chunks],
    metadatas=[c["metadata"] for c in processed_chunks],
    ids=[c["id"] for c in processed_chunks]
)

# 2. Initialize BM25 Index (Sparse)
tokenized_corpus = [c["text"].lower().split() for c in processed_chunks]
bm25_index = BM25Okapi(tokenized_corpus)

def reciprocal_rank_fusion(vector_results: List[str], bm25_results: List[str], k: int = 60) -> List[str]:
    """
    RRF Algorithm: Merges dense and sparse search rankings into a unified score.
    Score = sum( 1 / (k + rank_i) )
    """
    rrf_scores = {}
    
    # Process vector ranks
    for rank, doc in enumerate(vector_results):
        rrf_scores[doc] = rrf_scores.get(doc, 0.0) + (1.0 / (k + rank + 1))
        
    # Process BM25 ranks
    for rank, doc in enumerate(bm25_results):
        rrf_scores[doc] = rrf_scores.get(doc, 0.0) + (1.0 / (k + rank + 1))
        
    # Sort documents by score descending
    sorted_docs = sorted(rrf_scores.items(), key=lambda item: item[1], reverse=True)
    return [doc for doc, score in sorted_docs]

def hybrid_search(query: str, top_n: int = 4) -> List[str]:
    # A. Dense Vector Retrieval
    vector_res = vector_collection.query(query_texts=[query], n_results=top_n)['documents'][0]
    
    # B. Sparse BM25 Retrieval
    query_tokens = query.lower().split()
    bm25_res_docs = bm25_index.get_top_n(query_tokens, [c["text"] for c in processed_chunks], n=top_n)
    
    # C. Reciprocal Rank Fusion
    fused_results = reciprocal_rank_fusion(vector_res, bm25_res_docs)
    return fused_results[:top_n]

# Test Hybrid Search
query = "What is the part ID for Sunshield Replacement?"
print("Hybrid Search Results:")
for d in hybrid_search(query, top_n=2):
    print("-", d)
