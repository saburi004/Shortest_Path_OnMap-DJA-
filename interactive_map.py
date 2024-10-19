

import folium
import osmnx as ox
import networkx as nx

# Load the graph from the .graphml file
G = ox.load_graphml(filepath="pune.graphml")

# Get the center of the graph for initializing the map
graph_center = ox.graph_to_gdfs(G, nodes=True, edges=False).unary_union.centroid
lat, lon = graph_center.y, graph_center.x

# Create a map centered on the graph's center
m = folium.Map(location=[lat, lon], zoom_start=14)

# Add a click event to capture coordinates
click_handler = folium.LatLngPopup()
m.add_child(click_handler)

# Save the map with LatLngPopup
m.save("interactive_map.html")
print("Map created. Open 'interactive_map.html' to select points and copy coordinates.")
