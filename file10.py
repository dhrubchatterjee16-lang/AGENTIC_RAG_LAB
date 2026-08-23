from langgraph.graph import StateGraph, END

# Initialize Graph
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("route_question", route_question_node)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("grade_documents", grade_documents_node)
workflow.add_node("web_search", web_search_node)
workflow.add_node("generate", generate_node)
workflow.add_node("direct_answer", direct_answer_node)

# Set Entry Point
workflow.set_entry_point("route_question")

# Conditional Edge 1: Route based on intent
def route_decision_edge(state: AgentState):
    if state["route"] == "vectorstore":
        return "retrieve"
    elif state["route"] == "websearch":
        return "web_search"
    else:
        return "direct_answer"

workflow.add_conditional_edges(
    "route_question",
    route_decision_edge,
    {
        "retrieve": "retrieve",
        "web_search": "web_search",
        "direct_answer": "direct_answer"
    }
)

# Connect Retrieve -> Grade
workflow.add_edge("retrieve", "grade_documents")

# Conditional Edge 2: Check if Grader requested Web Search fallback
def grade_decision_edge(state: AgentState):
    if state["web_search_needed"]:
        return "web_search"
    else:
        return "generate"

workflow.add_conditional_edges(
    "grade_documents",
    grade_decision_edge,
    {
        "web_search": "web_search",
        "generate": "generate"
    }
)

# Connect Web Search -> Generate
workflow.add_edge("web_search", "generate")

# Connect Generators -> END
workflow.add_edge("generate", END)
workflow.add_edge("direct_answer", END)

# Compile Graph App
app = workflow.compile()
print("LangGraph Agentic RAG workflow successfully compiled!")
