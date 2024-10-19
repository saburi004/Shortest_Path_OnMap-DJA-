import osmnx as ox
import pandas as pd

# Load the graph from the GraphML file
G = ox.load_graphml(filepath="pune.graphml")

# Extract nodes and edges from the graph
nodes, edges = ox.graph_to_gdfs(G)

# Print the columns to understand the structure
print("Nodes columns:")                      #Edges columns:
                                             # Index(['osmid', 'highway', 'oneway', 'reversed', 'length', 'geometry', 'lanes',
                                             #        'name', 'ref', 'maxspeed', 'bridge', 'est_width', 'access', 'junction',
                                             #        'tunnel', 'width'],
                                             #       dtype='object') this is output
print(nodes.columns)

print("Edges columns:")
print(edges.columns)

# Save nodes to CSV
nodes[['y', 'x']].to_csv("nodes.csv", index_label="node_id")

# Save edges to CSV with osmid and length
edges[['osmid', 'length']].to_csv("edges.csv", index=False)
