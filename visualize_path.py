import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

# Load the graph
G = ox.load_graphml(filepath="pune.graphml")

# Example path (replace with actual path node IDs)
path = [0, 1, 2, 3, 4]

# Plot the route on the map
fig, ax = plt.subplots(figsize=(10, 10))
ox.plot_graph_route(G, path, ax=ax, route_linewidth=6, node_size=0, bgcolor='k')
plt.show()
