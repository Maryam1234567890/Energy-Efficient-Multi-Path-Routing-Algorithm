import networkx as nx
import heapq
import copy
import socket
import pickle

def energy_efficient_multipath_routing(G, source, dest, battery_capacity, threshold, num_paths=3):
    H = G.to_directed().reverse(copy=True)
    H.add_edges_from((v, u, H[u][v]) for u, v in H.edges())
    remaining_battery_capacity = copy.deepcopy(battery_capacity)
    shortest_path = nx.dijkstra_path(G, source, dest, weight='weight')
    paths_to_explore = []
    heapq.heappush(paths_to_explore, (-len(shortest_path), shortest_path))
    explored_paths = set()
    valid_paths = []
    while paths_to_explore and len(valid_paths) < num_paths:
        _, path = heapq.heappop(paths_to_explore)
        if tuple(path) in explored_paths: continue
        explored_paths.add(tuple(path))
        valid = True
        for node in path:
            if remaining_battery_capacity[node] < threshold:
                valid = False
                break
        if valid:
            for node in G.nodes:
                remaining_battery_capacity[node] -= threshold
            valid_paths.append(path)
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i+1]
                if remaining_battery_capacity[v] >= threshold:
                    H.add_edge(v, u, **G[u][v])
                    shortest_path_v_u = nx.dijkstra_path(H, v, u, weight='weight')
                    heapq.heappush(paths_to_explore, (-len(shortest_path_v_u), shortest_path_v_u))
                    H.remove_edge(v, u)
    return valid_paths

def serve():
    HOST = '' # Listen on all available interfaces
    PORT = 65432 # Arbitrary non-privileged port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print('Server started listening on port', PORT)
        while True:
            conn, addr = s.accept()
            print('Connected by', addr)
            data = conn.recv(1024)
            if not data:
                continue
            G, source, dest, battery_capacity, threshold, num_paths = pickle.loads(data)
            paths = energy_efficient_multipath_routing(G, source, dest, battery_capacity, threshold, num_paths)
            conn.sendall(pickle.dumps(paths))
