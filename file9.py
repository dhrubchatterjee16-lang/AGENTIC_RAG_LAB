from duckduckgo_search import DDGS

# 1. ROUTER NODE
def route_question_node(state: AgentState) -> AgentState:
    question = state["question"]

    prompt = f"""You are an expert router. Analyze the question and classify it into ONE of three categories:
1. 'vectorstore': Questions about Acme Corp policies, benefits, stipends, or security protocols.
2. 'websearch': Questions about current world events, weather, stock prices, news, or external technical topics.
3. 'direct': General greetings, chit-chat, or questions that don't need external data.

Return ONLY one word: 'vectorstore', 'websearch', or 'direct'.

QUESTION: {question}"""

    response = client.models.generate_content(model='gemini-3.6-flash', contents=prompt)
    route_decision = response.text.strip().lower()

    # Clean output
    if 'vector' in route_decision:
        state["route"] = 'vectorstore'
    elif 'web' in route_decision:
        state["route"] = 'websearch'
    else:
        state["route"] = 'direct'

    print(f"--- [ROUTER] Decision: '{state['route']}' ---")
    return state

# 2. VECTOR RETRIEVAL NODE
def retrieve_node(state: AgentState) -> AgentState:
    print("--- [RETRIEVE] Querying Vector Database ---")
    question = state["question"]
    results = vector_collection.query(query_texts=[question], n_results=2)
    state["documents"] = results['documents'][0]
    return state

# 3. DOCUMENT GRADER NODE (Filter Low-Quality Context)
def grade_documents_node(state: AgentState) -> AgentState:
    print("--- [GRADE] Evaluating Document Relevance ---")
    question = state["question"]
    documents = state["documents"]

    filtered_docs = []
    web_search_needed = False

    for doc in documents:
        prompt = f"""Evaluate if the following document is relevant to the question.
Respond with 'yes' if relevant, or 'no' if irrelevant.

DOCUMENT: {doc}
QUESTION: {question}"""
        res = client.models.generate_content(model='gemini-3.6-flash', contents=prompt)
        score = res.text.strip().lower()

        if 'yes' in score:
            filtered_docs.append(doc)
        else:
            print(" -> Filtered out irrelevant document snippet!")

    if len(filtered_docs) == 0:
        print(" -> All vector documents rejected! Triggering Web Search fallback.")
        web_search_needed = True

    state["documents"] = filtered_docs
    state["web_search_needed"] = web_search_needed
    return state

# 4. WEB SEARCH NODE (Fallback)
def web_search_node(state: AgentState) -> AgentState:
    print("--- [WEB SEARCH] Fetching live web search results ---")
    question = state["question"]

    results_text = ""
    with DDGS() as ddgs:
        results = list(ddgs.text(question, max_results=2))
        for r in results:
            results_text += f"{r['title']}: {r['body']}\n"

    state["documents"].append(results_text)
    return state

# 5. GENERATOR NODE
def generate_node(state: AgentState) -> AgentState:
    print("--- [GENERATE] Generating answer with Gemini ---")
    question = state["question"]
    documents = state["documents"]

    context = "\n\n".join(documents)
    prompt = f"""Answer the question based strictly on the provided context.

CONTEXT:
{context}

QUESTION: {question}"""

    response = client.models.generate_content(model='gemini-3.6-flash', contents=prompt)
    state["generation"] = response.text
    return state

# 6. DIRECT ANSWER NODE
def direct_answer_node(state: AgentState) -> AgentState:
    print("--- [DIRECT] Answering directly without retrieval ---")
    question = state["question"]
    response = client.models.generate_content(model='gemini-3.6-flash', contents=question)
    state["generation"] = response.text
    return state
