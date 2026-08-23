def crag_web_search_node(query: str) -> str:
    """
    Fetches real-time web search results using DuckDuckGo.
    """
    print(" 🌐 [CRAG Web Search] Fetching external web knowledge...")
    results_text = ""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            for r in results:
                results_text += f"Source: {r['title']}\nSummary: {r['body']}\n\n"
    except Exception as e:
        results_text = f"Web Search error: {e}"

    return results_text.strip()
