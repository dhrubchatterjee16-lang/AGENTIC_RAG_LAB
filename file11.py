def run_agent_query(query: str):
    print(f"\n==================================================")
    print(f"USER QUERY: '{query}'")
    print(f"==================================================")

    initial_state = {
        "question": query,
        "generation": "",
        "web_search_needed": False,
        "documents": [],
        "route": ""
    }

    output = app.invoke(initial_state)
    print(f"\nFINAL ANSWER:\n{output['generation']}\n")

# Scenario 1: Internal Policy Question (Vector DB Route)
run_agent_query("How much home office stipend does Acme Corp give?")

# Scenario 2: Out of Domain / Real-Time Question (Web Search Fallback Route)
run_agent_query("What is the latest release version of Python?")

# Scenario 3: General Chit-Chat (Direct Route)
run_agent_query("Hello! How can you help me today?")
