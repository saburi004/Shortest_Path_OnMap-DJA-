# Step 1 Download OSM Data #pip install osmnx pandas


import osmnx as ox

# Define the city or place name
place_name = 'Pune, India'

# Download the street network for driving (you can change the network type to 'bike', 'walk', etc.)
G = ox.graph_from_place(place_name, network_type='drive')

# Optionally, save the graph to a file for later use
ox.save_graphml(G, filepath="pune.graphml")
