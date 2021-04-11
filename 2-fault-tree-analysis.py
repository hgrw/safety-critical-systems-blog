import networkx as nx
import json
import cutsets

# Extract tree from graphml file
tree = nx.read_graphml('lib/simple-boolean-fault-tree.graphml')
nodes, edges = {}, {}

# Extract node data
for node in tree.nodes(data=True):
    nodes[node[0]] = json.loads(node[1]['label'])

# Extract edge data
for edge in tree.edges():
    edges[edge[0]] = edge[1]

# Construct data for cutsets
print('done')