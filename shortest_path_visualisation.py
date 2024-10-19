


from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import folium
import osmnx as ox
import networkx as nx
from geopy.geocoders import Nominatim

app = Flask(__name__)
CORS(app)

# Load the graph from the .graphml file
G = ox.load_graphml(filepath="pune.graphml")
geolocator = Nominatim(user_agent="shortest_path_finder")

def geocode_location(location_name):
    try:
        location = geolocator.geocode(location_name)
        if location:
            return (location.latitude, location.longitude)
        return None
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None

@app.route('/calculate_shortest_path', methods=['POST'])
def calculate_shortest_path():
    data = request.json
    source_name = data.get('source_name')
    destination_name = data.get('destination_name')

    # Geocode source and destination names to coordinates
    start_coords = geocode_location(source_name)
    end_coords = geocode_location(destination_name)

    if not start_coords or not end_coords:
        return jsonify({"error": "Invalid location names"}), 400

    start_node = ox.distance.nearest_nodes(G, X=start_coords[1], Y=start_coords[0])
    end_node = ox.distance.nearest_nodes(G, X=end_coords[1], Y=end_coords[0])

    # Calculate the shortest path
    shortest_path = nx.shortest_path(G, source=start_node, target=end_node, weight='length')
    route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in shortest_path]

    # Create a map centered on the graph's center
    graph_center = ox.graph_to_gdfs(G, nodes=True, edges=False).unary_union.centroid
    m = folium.Map(location=[graph_center.y, graph_center.x], zoom_start=14)

    # Plot the shortest path on the map
    folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.8).add_to(m)

    # Add markers for start and end points
    folium.Marker(location=[start_coords[0], start_coords[1]], popup=source_name).add_to(m)
    folium.Marker(location=[end_coords[0], end_coords[1]], popup=destination_name).add_to(m)

    # Save the result map to an HTML file
    map_file = "shortest_path_map.html"
    m.save(map_file)

    # Return the path of the map file to be served
    return jsonify({"message": "Shortest path calculated", "map_file": map_file}), 200

@app.route('/shortest_path_map')
def serve_map():
    return send_file("shortest_path_map.html")

if __name__ == '__main__':
    app.run(debug=True)


