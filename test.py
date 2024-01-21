import networkx as nx
import heapq
import copy

def energy_efficient_multipath_routing(G, source, dest, battery_capacity, threshold, num_paths=3):
    """
    An Energy Efficient Multi-Path Routing Algorithm.

    Args:
        G (networkx.Graph): the network topology represented as a graph
        source (int): the source node
        dest (int): the destination node
        battery_capacity (dict): a dictionary mapping each node to its battery capacity
        threshold (float): the threshold value for the remaining battery capacity
            below which a node is considered dead
        num_paths (int): the maximum number of paths to return

    Returns:
        A list of up to num_paths paths from the source to the destination
    """

    # Create a copy of the original graph and add reversed edges to it
    H = G.to_directed().reverse(copy=True) 
    #if isinstance(G, nx.DiGraph):
    #    H = G.reverse(copy=True) 
    #else:
    #    H = G.to_directed().reverse()

    H.add_edges_from((v, u, H[u][v]) for u, v in H.edges())

    # Initialize a dictionary to store the remaining battery capacity of each node
    remaining_battery_capacity = copy.deepcopy(battery_capacity)

    # Find the shortest path in the original graph using Dijkstra's algorithm
    shortest_path = nx.dijkstra_path(G, source, dest, weight='weight')

    # Initialize a priority queue to store the paths to explore in the reversed graph
    paths_to_explore = []
    heapq.heappush(paths_to_explore, (-len(shortest_path), shortest_path))

    # Initialize a set to store the explored paths in the reversed graph
    explored_paths = set()

    # Initialize a list to store the valid paths found so far
    valid_paths = []

    while paths_to_explore and len(valid_paths) < num_paths:

        # Pop the path with the highest priority from the queue
        _, path = heapq.heappop(paths_to_explore)

        # Check if the path has already been explored
        if tuple(path) in explored_paths:
            continue

        # Add the path to the set of explored paths
        explored_paths.add(tuple(path))

        # Check if the path avoids nodes with low battery capacity
        valid = True
        for node in path:
            if remaining_battery_capacity[node] < threshold:
                valid = False
                break

        if valid:

            # Update the remaining battery capacity of each node in the original graph
            for node in G.nodes:
                remaining_battery_capacity[node] -= threshold

            # Add the path to the list of valid paths
            valid_paths.append(path)

            # Update the priority queue with new paths to explore
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i+1]
                if remaining_battery_capacity[v] >= threshold:
                    # Add the edge (v, u) to the reversed graph
                    H.add_edge(v, u, **G[u][v])
                    # Find the shortest path from v to u in the reversed graph
                    shortest_path_v_u = nx.dijkstra_path(H, v, u, weight='weight')
                    # Add the path to the priority queue
                    heapq.heappush(paths_to_explore, (-len(shortest_path_v_u), shortest_path_v_u))

                    # Remove the edge (v, u) from the reversed graph
                    H.remove_edge(v, u)

    # Return the valid paths
    return valid_paths


# Create a network topology represented as a graph
G = nx.Graph()
G.add_edges_from([(1, 2, {'weight': 10}), (1, 3, {'weight': 5}), (2, 3, {'weight': 3}),
                  (2, 4, {'weight': 2}), (3, 4, {'weight': 7}), (3, 5, {'weight': 5}),
                  (4, 5, {'weight': 10}), (4, 6, {'weight': 1}), (5, 6, {'weight': 2})])

# Define the battery capacity of each node
battery_capacity = {1: 100, 2: 80, 3: 70, 4: 50, 5: 30, 6: 10}

# Set the threshold value for the remaining battery capacity
threshold = 20

# Define the source and destination nodes
source = 1
dest = 4

# Run the Energy Efficient Multi-Path Routing Algorithm
paths = energy_efficient_multipath_routing(G, source, dest, battery_capacity, threshold, num_paths=3)

# Print the paths
print(paths)
