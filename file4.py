def crag_evaluator_node(query: str, retrieved_docs: list) -> tuple[str, float]:
    """
    CRAG Evaluator Node: Assigns confidence score and decides CRAG Action Path.
    """
    if not retrieved_docs:
        return "INCORRECT", 0.0

    combined_docs = "\n".join(retrieved_docs)

    prompt = f"""Evaluate the retrieved document context against the user query.
Determine the confidence score from 0.0 to 1.0 based on how well the documents answer the query.

Rules:
- Score > 0.7 -> 'CORRECT' (Documents contain exact, complete information)
- Score 0.3 to 0.7 -> 'AMBIGUOUS' (Documents are partially related or missing key details)
- Score < 0.3 -> 'INCORRECT' (Documents are irrelevant or wrong)

Return JSON format ONLY:
{{"score": 0.85, "action": "CORRECT", "reason": "Explanation"}}

QUERY: {query}
CONTEXT:
{combined_docs}"""

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )

    try:
        clean_json = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_json)
        action = data.get("action", "INCORRECT").upper()
        score = float(data.get("score", 0.0))
        return action, score
    except Exception as e:
        print(f"Error parsing evaluator: {e}")
        return "INCORRECT", 0.0
