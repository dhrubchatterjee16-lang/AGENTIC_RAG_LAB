def generate_graph_rag_answer(query: str) -> str:
    # 1. Retrieve Graph Multi-Hop Context
    relational_context = retrieve_graph_context(query, depth=3)
    
    # 2. Construct GraphRAG Augmented Prompt
    prompt = f"""You are an advanced GraphRAG Reasoning System. 
Answer the user query by analyzing the step-by-step entity relationship chain extracted from the Knowledge Graph.

RELATIONAL KNOWLEDGE GRAPH CONTEXT:
----------------------------------
{relational_context}
----------------------------------

USER QUERY: {query}

Explain the step-by-step causal relationship chain in your final answer."""

    # 3. Generate Answer
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    
    return response.text

# Test Multi-Hop Query
multi_hop_query = "Why is Smartphone X1 experiencing supply delays because of MiningCo Global?"
answer = generate_graph_rag_answer(multi_hop_query)

print("\n=== GraphRAG MULTI-HOP REASONING ANSWER ===")
print(answer)
