def retrieve_graph_context(query: str, depth: int = 2) -> str:
    """
    Extracts seed entities mentioned in the query and traverses the Knowledge Graph up to N hops deep.
    """
    # 1. Identify seed nodes mentioned in query
    query_lower = query.lower()
    seed_nodes = [node for node in KG.nodes if node.lower() in query_lower]
    
    if not seed_nodes:
        # Fallback: Search nodes with partial keyword matches
        for node in KG.nodes:
            for word in query.split():
                if len(word) > 3 and word.lower() in node.lower():
                    seed_nodes.append(node)
                    
    seed_nodes = list(set(seed_nodes))
    print(f"Detected Seed Graph Entities: {seed_nodes}")
    
    # 2. Traverse N-hop neighbors from seed nodes
    subgraph_triples = []
    visited_edges = set()
    
    for seed in seed_nodes:
        # Get ego graph (neighbors up to 'depth' distance)
        ego_g = nx.ego_graph(KG, seed, radius=depth, undirected=True)
        for u, v, data in ego_g.edges(data=True):
            edge_key = (u, v, data.get('relation', ''))
            if edge_key not in visited_edges:
                visited_edges.add(edge_key)
                subgraph_triples.append(f"{u} -> {data.get('relation', 'RELATED_TO')} -> {v}")
                
    return "\n".join(subgraph_triples)

# Test Subgraph Retrieval
test_q = "How did the MiningCo Global flood affect Smartphone X1?"
graph_context = retrieve_graph_context(test_q, depth=3)

print(f"\nRetrieved Graph Relational Context:\n{graph_context}")
