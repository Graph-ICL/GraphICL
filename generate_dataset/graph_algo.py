import networkx as nx
from networkx.algorithms import isomorphism
import re
import itertools
from collections import deque
from collections import defaultdict


def extract_edges_a(input_str):
    edges_start = input_str.find("edges are:")
    if edges_start == -1:
        raise ValueError("'edges are:' not found")
    edges_str = input_str[edges_start + len("edges are:"):].split(".")[0].strip()
    edges = []
    for edge in edges_str.split(")"):
        edge = edge.strip()
        if not edge:
            continue
        edge = edge.lstrip("(")
        nodes = edge.split(",")
        if len(nodes) != 2:
            continue
        try:
            u = int(nodes[0].strip())
            v = int(nodes[1].strip())
            edges.append((u, v))
        except ValueError:
            continue
    return edges


def extract_edges_b(input_str):
    edges_start = input_str.find("edges are:")
    if edges_start == -1:
        raise ValueError("'edges are:' not found")
    edges_str = input_str[edges_start + len("edges are:"):].split(".")[0].strip()
    edges = []
    for edge in edges_str.split():
        edge = edge.strip("()")
        if not edge:
            continue
        nodes = edge.split("->")
        if len(nodes) != 2:
            continue
        try:
            u = int(nodes[0].strip())
            v = int(nodes[1].strip())
            edges.append((u, v))
        except ValueError:
            continue
    return edges


def extract_edges_c(input_str):
    edges_start = input_str.find("edges are:")
    if edges_start == -1:
        raise ValueError("'edges are:' not found")
    edges_str = input_str[edges_start + len("edges are:"):].split(".")[0].strip()
    edges = []
    for edge in edges_str.split():
        edge = edge.strip("(),")
        if not edge:
            continue
        parts = edge.split(",")
        if len(parts) != 3:
            continue
        try:
            u = int(parts[0].strip())
            v = int(parts[1].strip())
            w = int(parts[2].strip())
            edges.append((u, v, w))
        except ValueError:
            continue
    return edges


def extract_edges_d(input_str):
    matches = re.findall(r'\(\s*(\d+)\s*->\s*(\d+)\s*,\s*(\d+)\s*\)', input_str)
    edges = [(int(i), int(j), int(k)) for i, j, k in matches]
    return edges


def extract_edges_subgraph(input_str):
    g_edges_matches = re.findall(r'\(\s*(\d+)\s*->\s*(\d+)\s*\)', input_str)
    g_edges = [(int(u), int(v)) for u, v in g_edges_matches]
    edges_start = input_str.find("edges are:")
    if edges_start == -1:
        raise ValueError("No 'edges are:' found")
    edges_start = input_str.find("edges are:", edges_start + 1)
    if edges_start == -1:
        raise ValueError("No second 'edges are:' found")
    g_prime_edges_matches = re.findall(r'\(\s*([a-o])\s*->\s*([a-o])\s*\)', input_str[edges_start:])
    g_prime_edges = [(u, v) for u, v in g_prime_edges_matches]
    return g_edges, g_prime_edges


def extract_nodes(input_str):
    edges_start = input_str.find("edges are:")
    if edges_start == -1:
        raise ValueError("No 'edges are:' found")
    question = input_str[edges_start + len("edges are:"):].split(".")[1].strip()
    node_part = question.split("node")[1:]
    if len(node_part) < 2:
        raise ValueError("Two nodes not found")
    node1 = int(node_part[0].strip().split()[0])
    number2 = re.search(r"\d+", node_part[1].strip().split()[0]).group()
    node2 = int(number2)
    return node1, node2


def extract_node_weights(input_str):
    matches = re.findall(r'\[\s*(\d+)\s*,\s*(\d+)\s*\]', input_str)
    node_weights = [[int(i), int(k)] for i, k in matches]
    return node_weights


def extract_node_num(input_str):
    node_range_match = re.search(r'nodes are numbered from (\d+) to (\d+)', input_str)
    if node_range_match:
        start_node = int(node_range_match.group(1))
        end_node = int(node_range_match.group(2))
        num_nodes = end_node - start_node + 1
    else:
        num_nodes = 0
    return num_nodes


def has_cycle(edges):
    G = nx.Graph()
    G.add_edges_from(edges)
    try:
        nx.find_cycle(G)
        return "### Yes"
    except nx.NetworkXNoCycle:
        return "### No"


def are_nodes_connected(edges, node1, node2):
    G = nx.Graph()
    all_nodes = set()
    for u, v in edges:
        all_nodes.add(u)
        all_nodes.add(v)
    G.add_nodes_from(all_nodes)
    G.add_edges_from(edges)
    if node1 not in G or node2 not in G:
        return "### No"
    if nx.has_path(G, node1, node2):
        return "### Yes"
    else:
        return "### No"


def is_bipartite(edges):
    G = nx.DiGraph()
    G.add_edges_from(edges)
    G_undirected = G.to_undirected()
    if nx.is_bipartite(G_undirected):
        return "### Yes"
    else:
        return "### No"


def topological_sort(edges):
    G = nx.DiGraph()
    G.add_edges_from(edges)
    try:
        sorted_nodes = list(nx.topological_sort(G))
        return "### " + str(sorted_nodes)
    except nx.NetworkXUnfeasible:
        return "### The graph has rings and cannot be topologically sorted"


def shortest_path_weight(edges, node1, node2):
    G = nx.Graph()
    all_nodes = set()
    for u, v, w in edges:
        all_nodes.add(u)
        all_nodes.add(v)
    G.add_nodes_from(all_nodes)
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
    if node1 not in G or node2 not in G:
        return "### There is no path between nodes"
    try:
        weight = nx.dijkstra_path_length(G, node1, node2)
        return "### " + str(weight)
    except nx.NetworkXNoPath:
        return "### There is no path between nodes"


def max_weight_of_triangle(node_weights, edges):
    G = nx.Graph()
    for u, v in edges:
        G.add_edge(u, v)
    weights = {node: weight for node, weight in node_weights}
    max_sum = -float("inf")
    for u in G.nodes:
        for v in G.neighbors(u):
            for w in G.neighbors(v):
                if G.has_edge(u, w):
                    current_sum = weights[u] + weights[v] + weights[w]
                    if current_sum > max_sum:
                        max_sum = current_sum
    return "### " + str(max_sum) if max_sum != -float("inf") else "### No triples satisfy the condition"


def max_flow(edges, source, target):
    G = nx.DiGraph()
    all_nodes = set()
    for u, v, w in edges:
        all_nodes.add(u)
        all_nodes.add(v)
    G.add_nodes_from(all_nodes)
    for u, v, w in edges:
        G.add_edge(u, v, capacity=w)
    if source not in G or target not in G:
        return "### 0"
    flow_value, flow_dict = nx.maximum_flow(G, source, target)
    return "### " + str(flow_value)


def has_hamiltonian_path(edges, num_nodes):
    G = nx.Graph()
    G.add_edges_from(edges)
    if num_nodes == 0:
        return "### No"
    if num_nodes == 1:
        return "### Yes"
    if not nx.is_connected(G):
        return "### No"
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    dp = [[False] * num_nodes for _ in range(1 << num_nodes)]
    for i in range(num_nodes):
        dp[1 << i][i] = True
    for mask in range(1 << num_nodes):
        for u in range(num_nodes):
            if dp[mask][u]:
                for v in graph[u]:
                    if not (mask & (1 << v)):
                        dp[mask | (1 << v)][v] = True
    for u in range(num_nodes):
        if dp[(1 << num_nodes) - 1][u]:
            return "### Yes"
    return "### No"


def is_subgraph(G_edges, G_prime_edges):
    G = nx.DiGraph()
    G.add_edges_from(G_edges)
    G_prime = nx.DiGraph()
    G_prime.add_edges_from(G_prime_edges)
    G_nodes = list(G.nodes())
    G_prime_nodes = list(G_prime.nodes())
    if len(G_prime_nodes) > len(G_nodes):
        return "### No"
    for mapping_nodes in itertools.permutations(G_nodes, len(G_prime_nodes)):
        mapping = {G_prime_nodes[i]: mapping_nodes[i] for i in range(len(G_prime_nodes))}
        is_valid = True
        for edge in G_prime_edges:
            mapped_edge = (mapping[edge[0]], mapping[edge[1]])
            if mapped_edge not in G_edges:
                is_valid = False
                break
        if is_valid:
            return f"### Yes"
    return "### No"
```
