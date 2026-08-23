# Create Directed Graph
KG = nx.DiGraph()

# Populate Nodes and Directed Edges
for t in triples:
    subj = t['subject'].strip()
    obj = t['object'].strip()
    rel = t['relation'].strip()
    KG.add_edge(subj, obj, relation=rel)

print(f"Graph Created: {KG.number_of_nodes()} Nodes, {KG.number_of_edges()} Edges")

# Render Visual Graph in Colab
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(KG, k=0.9, iterations=50)

# Draw Nodes & Edges
nx.draw_networkx_nodes(KG, pos, node_color='skyblue', node_size=2500)
nx.draw_networkx_edges(KG, pos, edge_color='gray', arrows=True, arrowsize=20, width=2)
nx.draw_networkx_labels(KG, pos, font_size=10, font_family='sans-serif', font_weight='bold')

# Draw Edge Labels (Relationships)
edge_labels = nx.get_edge_attributes(KG, 'relation')
nx.draw_networkx_edge_labels(KG, pos, edge_labels=edge_labels, font_size=8)

plt.title("Extracted Knowledge Graph Visualization", fontsize=14)
plt.axis('off')
plt.show()
