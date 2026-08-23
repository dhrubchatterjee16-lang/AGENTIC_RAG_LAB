def decompose_and_filter_strips(query: str, documents: list) -> list:
    """
    Decomposes documents into sentence-level knowledge strips and filters out noise.
    """
    # 1. Decompose docs into individual sentence strips
    strips = []
    for doc in documents:
        sentences = re.split(r'(?<=[.!?]) +', doc)
        for s in sentences:
            if len(s.strip()) > 10:
                strips.append(s.strip())

    # 2. Filter strips using Gemini Grader
    relevant_strips = []
    for strip in strips:
        prompt = f"""Is the following sentence relevant to answering the query?
Sentence: "{strip}"
Query: "{query}"

Respond with JSON: {{"relevant": true}} or {{"relevant": false}}"""

        res = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        try:
            clean_json = res.text.replace("```json", "").replace("```", "").strip()
            result = json.loads(clean_json)
            if result.get("relevant", False):
                relevant_strips.append(strip)
        except:
            relevant_strips.append(strip)

    return relevant_strips
