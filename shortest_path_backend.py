from flask import Flask, request, jsonify
import osmnx as ox
import networkx as nx

app = Flask(__name__)

# Load the graph from the .graphml file (as in your code)
G = ox.load_graphml(filepath="pune.graphml")

@app.route('/calculate_shortest_path', methods=['POST'])
def calculate_shortest_path():
    data = request.json
    new_lat = data['lat']
    new_lng = data['lng']
    
    # Start node (keep original start node)
    start_coords = [18.4552, 73.8724]  # Replace with actual start coordinates
    start_node = ox.distance.nearest_nodes(G, X=start_coords[1], Y=start_coords[0])

    # Find the nearest node to the clicked point
    end_node = ox.distance.nearest_nodes(G, X=new_lng, Y=new_lat)

    # Calculate the shortest path
    shortest_path = nx.shortest_path(G, source=start_node, target=end_node, weight='length')

    # Get route coordinates
    route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in shortest_path]

    # Send the route coordinates back to the frontend
    return jsonify({
        "route_coords": route_coords
    })

if __name__ == '__main__':
    app.run(debug=True)
