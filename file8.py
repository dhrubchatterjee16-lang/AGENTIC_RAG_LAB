from typing import List, TypedDict

class AgentState(TypedDict):
    question: str
    generation: str
    web_search_needed: bool
    documents: List[str]
    route: str  # 'vectorstore', 'websearch', or 'direct'
