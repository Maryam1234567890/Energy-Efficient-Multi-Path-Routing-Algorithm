import socket
import pickle
import networkx as nx

def energy_efficient_multipath_routing_client():
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
    source = 5
    dest = 2

    # Set the maximum number of paths to return
    num_paths = 3

    # Create a dictionary containing the input arguments
    args = {
        'G': G,
        'source': source,
        'dest': dest,
        'battery_capacity': battery_capacity,
        'threshold': threshold,
        'num_paths': num_paths
    }

    # Serialize the dictionary
    data = pickle.dumps(args)

    # Create a socket and connect to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 10000)
    sock.connect(server_address)

    try:
        # Send the serialized data to the server
        sock.sendall(data)

        # Receive the result from the server
        result = sock.recv(1024)

        # Deserialize the result
        paths = pickle.loads(result)

        # Print the paths
        print(paths)
    finally:
        # Close the socket
        sock.close()


if __name__ == '__main__':
    energy_efficient_multipath_routing_client()
