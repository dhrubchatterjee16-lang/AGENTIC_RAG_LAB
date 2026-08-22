def retrieve_relevant_context(query: str, top_k: int = 2) -> List[str]:
    """
    Queries ChromaDB to find the most relevant text chunks for a given query.
    """
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    # Extract matching text snippets
    retrieved_chunks = results['documents'][0]
    return retrieved_chunks

# Test Retrieval
user_query = "What is the primary mirror of JWST made of?"
retrieved_docs = retrieve_relevant_context(user_query, top_k=2)

print(f"Query: '{user_query}'\n")
print("Retrieved Context:")
for idx, doc in enumerate(retrieved_docs, 1):
    print(f"[{idx}] {doc}")
