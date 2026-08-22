from sentence_transformers import CrossEncoder

# Load a fast pre-trained Cross-Encoder model
reranker_model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank_documents(query: str, candidate_docs: List[str], top_k: int = 2) -> List[str]:
    """
    Re-ranks candidate documents using Cross-Encoder scoring.
    """
    if not candidate_docs:
        return []
        
    # Build query-document pairs
    pairs = [[query, doc] for doc in candidate_docs]
    
    # Predict relevance scores
    scores = reranker_model.predict(pairs)
    
    # Pair scores with documents and sort
    doc_score_pairs = list(zip(candidate_docs, scores))
    sorted_pairs = sorted(doc_score_pairs, key=lambda x: x[1], reverse=True)
    
    return [doc for doc, score in sorted_pairs[:top_k]]

# Test Two-Stage Pipeline
candidates = hybrid_search(query, top_n=4)
final_reranked = rerank_documents(query, candidates, top_k=2)

print("Top Reranked Context:")
for idx, doc in enumerate(final_reranked, 1):
    print(f"[{idx}] {doc}")
