def run_crag_pipeline(query: str):
    print(f"\n==================================================")
    print(f"USER QUERY: '{query}'")
    print(f"==================================================")

    # Step 1: Retrieve from Vector DB
    vector_results = vector_store.query(query_texts=[query], n_results=2)['documents'][0]
    print(f"Step 1: Retrieved {len(vector_results)} raw vector documents.")

    # Step 2: CRAG Evaluator Node
    action_path, confidence_score = crag_evaluator_node(query, vector_results)
    print(f"Step 2: CRAG Evaluator -> Action Path: [{action_path}] (Confidence Score: {confidence_score:.2f})")

    final_context = ""

    # Step 3: Execute Action Paths
    if action_path == "CORRECT":
        print(" -> Action: Filtering Knowledge Strips from Vector DB...")
        strips = decompose_and_filter_strips(query, vector_results)
        final_context = "\n".join(strips)

    elif action_path == "AMBIGUOUS":
        print(" -> Action: Combining Vector Knowledge Strips + External Web Search...")
        strips = decompose_and_filter_strips(query, vector_results)
        web_context = crag_web_search_node(query)
        final_context = "--- Vector Knowledge Strips ---\n" + "\n".join(strips) + "\n\n--- External Web Context ---\n" + web_context

    else:  # INCORRECT
        print(" -> Action: Discarding Vector Docs completely! Relying 100% on Web Search...")
        web_context = crag_web_search_node(query)
        final_context = web_context

    # Step 4: Generate Final Answer with Gemini
    gen_prompt = f"""You are an expert technical assistant. Answer the user query strictly using the provided context.

CONTEXT:
{final_context}

QUERY: {query}"""

    answer = client.models.generate_content(model='gemini-2.5-flash', contents=gen_prompt).text
    return answer, action_path
