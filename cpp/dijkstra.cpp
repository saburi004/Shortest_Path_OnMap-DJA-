#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <queue>
#include <limits>
#include <string>

using namespace std;

typedef pair<int, double> pii;  // Pair of (node, weight)

// Function to load nodes from CSV
unordered_map<int, pair<double, double>> loadNodes(const string& filename) {
    unordered_map<int, pair<double, double>> nodes;
    ifstream file(filename);
    string line;
    getline(file, line);  // Skip header

    int node_id;
    double lat, lon;
    while (getline(file, line)) {
        stringstream ss(line);
        string token;
        getline(ss, token, ',');
        node_id = stoi(token);
        getline(ss, token, ',');
        lat = stod(token);
        getline(ss, token, ',');
        lon = stod(token);
        nodes[node_id] = {lat, lon};
    }
    return nodes;
}

// Function to load edges from CSV
vector<vector<pii>> loadEdges(const string& filename, int numNodes) {
    vector<vector<pii>> adjList(numNodes);
    ifstream file(filename);
    string line;
    getline(file, line);  // Skip header

    int source, target;
    double length;
    while (getline(file, line)) {
        stringstream ss(line);
        string token;
        getline(ss, token, ',');
        source = stoi(token);
        getline(ss, token, ',');
        target = stoi(token);
        getline(ss, token, ',');
        length = stod(token);

        adjList[source].push_back({target, length});
        adjList[target].push_back({source, length});  // Assuming undirected graph
    }
    return adjList;
}

// Dijkstra's Algorithm
vector<double> dijkstra(int start, int numNodes, const vector<vector<pii>>& adjList) {
    vector<double> dist(numNodes, numeric_limits<double>::max());
    dist[start] = 0.0;

    priority_queue<pii, vector<pii>, greater<pii>> pq;
    pq.push({0.0, start});

    while (!pq.empty()) {
        double d = pq.top().first;
        int u = pq.top().second;
        pq.pop();

        if (d > dist[u]) continue;

        for (const auto& neighbor : adjList[u]) {
            int v = neighbor.first;
            double weight = neighbor.second;

            if (dist[v] > dist[u] + weight) {
                dist[v] = dist[u] + weight;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}

int main() {
    int numNodes = 1000;  // Adjust as necessary based on your data

    // Load data
    auto nodes = loadNodes("nodes.csv");
    auto adjList = loadEdges("edges.csv", numNodes);

    int startNode = 0;  // Replace with your start node
    int endNode = 100;  // Replace with your end node

    // Run Dijkstra's algorithm
    vector<double> distances = dijkstra(startNode, numNodes, adjList);

    // Print the shortest path distance
    if (distances[endNode] != numeric_limits<double>::max()) {
        cout << "Shortest path from node " << startNode << " to node " << endNode << " is " << distances[endNode] << " meters." << endl;
    } else {
        cout << "No path from node " << startNode << " to node " << endNode << "." << endl;
    }

    return 0;
}
