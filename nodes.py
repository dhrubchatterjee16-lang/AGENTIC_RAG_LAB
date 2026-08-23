def extract_knowledge_triples(text: str):
    """
    Uses Gemini to parse unstructured text into structured entity-relation triples.
    """
    prompt = f"""You are a Knowledge Graph Extraction System. Extract all key relationships from the text as a JSON array of triples.
Each triple MUST have: "subject", "relation", and "object".

Return ONLY a JSON array without markdown formatting.

TEXT:
{text}

Example JSON output format:
[
  {{"subject": "TechCorp", "relation": "MANUFACTURES", "object": "Smartphone X1"}},
  {{"subject": "Smartphone X1", "relation": "USES_CHIP", "object": "M2-Microchip"}}
]"""

    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt
    )
    
    clean_json = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(clean_json)

# Extract Triples
triples = extract_knowledge_triples(corpus_text)
print(f"Extracted {len(triples)} Knowledge Triples:\n")
for t in triples:
    print(f"({t['subject']}) ──[{t['relation']}]──> ({t['object']})")
