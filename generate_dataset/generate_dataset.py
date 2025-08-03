import os
import utils
import graph_algo
import random
import networkx as nx
import shutil


def generate_cycle_question(task):
    query = task['query']
    node_num = graph_algo.extract_node_num(query)
    edges = task['edges']
    node_range_desc = f"The nodes are numbered from 0 to {node_num - 1}"
    edges_desc = "(" + ") (".join([f"{u}, {v}" for u, v, _ in edges]) + ")"
    new_query = (
        f"Determine whether or not there is a cycle in an undirected graph. "
        f"In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge. "
        f"Given a graph, you need to output Yes or No, indicating whether there is a cycle in the graph. "
        f"Q: {node_range_desc}, and the edges are: {edges_desc}. Is there a cycle in this graph?"
    )
    return new_query


def generate_connectivity_question(task, dataset_type, used_pairs=None):
    query = task['query']
    if used_pairs is None:
        used_pairs = set()
    node_num = graph_algo.extract_node_num(query)
    all_pairs = set()
    for x in range(node_num):
        for y in range(x + 1, node_num):
            all_pairs.add((x, y))
    if used_pairs.issuperset(all_pairs):
        return None, used_pairs
    available_pairs = all_pairs - used_pairs
    x, y = random.choice(list(available_pairs))
    used_pairs.add((x, y))
    question = f"Is there a path between node {x} and node {y}?"
    if dataset_type == 1:
        last_period_index = query.rfind('.')
        if last_period_index != -1:
            prefix = query[:last_period_index + 1]
            new_query = f"{prefix} {question}"
        else:
            raise ValueError("No period found")
    elif dataset_type == 2:
        node_range_desc = f"The nodes are numbered from 0 to {node_num - 1}"
        edges_desc = "(" + ") (".join([f"{u}, {v}" for u, v, _ in task['edges']]) + ")"
        new_query = (
            f"Determine whether two nodes are connected in an undirected graph. "
            f"In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge. "
            f"Given a graph and a pair of nodes, you need to output Yes or No, indicating whether the node i and node j are connected. "
            f"Q: {node_range_desc}, and the edges are: {edges_desc}. {question}"
        )
    return new_query, used_pairs


def generate_bipartite_question(task):
    query = task['query']
    node_num = graph_algo.extract_node_num(query)
    edges = task['edges']
    node_range_desc = f"The nodes are numbered from 0 to {node_num - 1}"
    edges_desc = "(" + ") (".join([f"{u}->{v}" for u, v, _ in edges]) + ")"
    new_query = (
        f"Determine whether or not a graph is bipartite. "
        f"In a directed graph, (i->j) means that node i and node j are connected with a directed edge from node i to node j. "
        f"Given a graph, you need to output Yes or No, indicating whether the graph is bipartite. "
        f"Q: {node_range_desc}, and the edges are: {edges_desc}. Is this graph bipartite?"
    )
    return new_query


def generate
