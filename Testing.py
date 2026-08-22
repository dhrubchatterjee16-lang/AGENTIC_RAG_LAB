# Test Query 1: Fact in document
query_1 = "What temperature does the telescope operate at?"
answer_1, context_1 = generate_rag_answer(query_1)

print("=== TEST 1 ===")
print(f"Question: {query_1}")
print(f"\nRetrieved Context:\n- " + "\n- ".join(context_1))
print(f"\nAnswer:\n{answer_1}")

print("\n" + "="*50 + "\n")

# Test Query 2: Out of context question (Hallucination Prevention test)
query_2 = "Who is the director of NASA?"
answer_2, context_2 = generate_rag_answer(query_2)

print("=== TEST 2 ===")
print(f"Question: {query_2}")
print(f"\nAnswer:\n{answer_2}")
