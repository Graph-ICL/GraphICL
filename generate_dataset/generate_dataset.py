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


def generate_topology_sort_question(task):
    query = task['query']
    node_num = graph_algo.extract_node_num(query)
    edges = task['edges']
    node_range_desc = f"The nodes are numbered from 0 to {node_num - 1}"
    edges_desc = "(" + ") (".join([f"{u}->{v}" for u, v, _ in edges]) + ")"
    new_query = (
        f"Find one of the topology sorting paths of the given graph. "
        f"In a directed graph, (i->j) means that node i and node j are connected with a directed edge from node i to node j. "
        f"Given a graph, you need to output one of the topology sorting paths of the graph. "
        f"Q: {node_range_desc}, and the edges are: {edges_desc}. Give one topology sorting path of this graph."
    )
    return new_query


def generate_shortest_path_question(task, dataset_type, used_pairs=None):
    query = task['query']
    if used_pairs is None:
        used_pairs = set()
    if dataset_type == 1:
        edges = graph_algo.extract_edges_c(query)
    elif dataset_type == 2:
        edges = task['edges']
    node_num = graph_algo.extract_node_num(query)
    G = nx.Graph()
    G.add_nodes_from(range(0, node_num))
    G.add_weighted_edges_from(edges)
    all_pairs = set()
    for x in range(node_num):
        for y in range(x + 1, node_num):
            all_pairs.add((x, y))
    all_connected_pairs = set()
    for x, y in all_pairs:
        if nx.has_path(G, x, y):
            all_connected_pairs.add((x, y))
    if used_pairs.issuperset(all_pairs):
        return None, used_pairs
    available_connected_pairs = all_connected_pairs - used_pairs
    if available_connected_pairs:
        x, y = random.choice(list(available_connected_pairs))
    else:
        available_disconnected_pairs = all_pairs - used_pairs - all_connected_pairs
        if not available_disconnected_pairs:
            return None, used_pairs
        x, y = random.choice(list(available_disconnected_pairs))
    used_pairs.add((x, y))
    question = f"Give the weight of the shortest path from node {x} to node {y}."
    if dataset_type == 1:
        last_period_index = query.rfind('.')
        if last_period_index == -1:
            raise ValueError("No period found")
        second_last_period_index = query.rfind('.', 0, last_period_index)
        if second_last_period_index != -1:
            prefix = query[:second_last_period_index + 1]
            new_query = f"{prefix} {question}"
        else:
            raise ValueError("No second period found")
    elif dataset_type == 2:
        node_range_desc = f"The nodes are numbered from 0 to {node_num - 1}"
        edges_desc = "(" + ") (".join([f"{u},{v},{w}" for u, v, w in edges]) + ")"
        new_query = (
            f"Find the shortest path between two nodes in an undirected graph. "
            f"In an undirected graph, (i,j,k) means that node i and node j are connected with an undirected edge with weight k. "
            f"Given a graph and a pair of nodes, you need to output the weight of the shortest path between the two nodes. "
            f"Q: {node_range_desc}, and the edges are: {edges_desc}. {question}"
        )
    return new_query, used_pairs


def generate_max_flow_question(query, used_pairs=None):
    if used_pairs is None:
        used_pairs = set()
    node_num = graph_algo.extract_node_num(query)
    edges = graph_algo.extract_edges_d(query)
    G = nx.DiGraph()
    G.add_nodes_from(range(0, node_num))
    G.add_weighted_edges_from(edges)
    all_pairs = set()
    for x in range(node_num):
        for y in range(node_num):
            if x != y:
                all_pairs.add((x, y))
    all_connected_pairs = set()
    for x, y in all_pairs:
        if nx.has_path(G, x, y):
            all_connected_pairs.add((x, y))
    if used_pairs.issuperset(all_pairs):
        return None, used_pairs
    available_connected_pairs = all_connected_pairs - used_pairs
    if available_connected_pairs:
        source, target = random.choice(list(available_connected_pairs))
    else:
        available_disconnected_pairs = all_pairs - used_pairs - all_connected_pairs
        if not available_disconnected_pairs:
            return None, used_pairs
        source, target = random.choice(list(available_disconnected_pairs))
    used_pairs.add((source, target))
    question = f"What is the maximum flow from node {source} to node {target}?"
    last_period_index = query.rfind('.')
    if last_period_index != -1:
        prefix = query[:last_period_index + 1]
        new_query = f"{prefix} {question}"
    else:
        raise ValueError("No period found")
    return new_query, used_pairs


def generate_hamiltonian_path_question(task):
    query = task['query']
    node_num = graph_algo.extract_node_num(query)
    edges = task['edges']
    node_range_desc = f"The nodes are numbered from 0 to {node_num - 1}"
    edges_desc = "(" + ") (".join([f"{u}, {v}" for u, v, _ in edges]) + ")"
    new_query = (
        f"Determine whether or not there is a Hamiltonian path in an undirected graph. "
        f"In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge. "
        f"Given a graph, you need to output Yes or No, indicating whether there is a Hamiltonian path in the graph. "
        f"Q: {node_range_desc}, and the edges are: {edges_desc}. Is there a Hamiltonian path in this graph?"
    )
    return new_query


def remove_random_edge(task, used_pairs=None):
    original_edges = task['edges']
    if used_pairs is None:
        used_pairs = set()
    available_edges = [edge for edge in original_edges if tuple(edge) not in used_pairs]
    if not available_edges:
        return None, used_pairs
    removed_edge = random.choice(available_edges)
    used_pairs.add(tuple(removed_edge))
    new_edges = [edge for edge in original_edges if edge != removed_edge]
    new_task = task.copy()
    new_task['edges'] = new_edges
    new_task['removed_edge'] = removed_edge
    return new_task, used_pairs


def generate_dataset1():
    flag_sampled1 = True
    if not flag_sampled1:
        utils.sample_dataset1()
    generate_size = 15
    sample_path = "sampled-dataset1"
    STR_sampled_ = "sampled_"
    task_list = ['connectivity', 'flow', 'shortest']
    dataset_path = 'dataset1'
    for task_name in task_list:
        sampled_file = f"{sample_path}/{STR_sampled_}{task_name}.json"
        sampled_tasks = utils.load_data(sampled_file)
        new_tasks = []
        for task in sampled_tasks:
            new_tasks.append(task)
            used_pairs = None
            for _ in range(generate_size):
                new_task = task.copy()
                if task_name == 'connectivity':
                    new_question, used_pairs = generate_connectivity_question(new_task, 1, used_pairs)
                elif task_name == 'flow':
                    new_question, used_pairs = generate_max_flow_question(new_task['query'], used_pairs)
                elif task_name == 'shortest':
                    new_question, used_pairs = generate_shortest_path_question(new_task, 1, used_pairs)
                if new_question is None:
                    continue
                new_task["query"] = new_question
                new_tasks.append(new_task)
        output_file = f"{dataset_path}/generated_{task_name}.json"
        utils.save_data(new_tasks, output_file)
        print(f"Generated {len(new_tasks)} new tasks, saved to {output_file}")


def generate_dataset2():
    flag_sampled2 = True
    if not flag_sampled2:
        utils.sample_dataset2()
    sample_path = "sampled-dataset2"
    STR_sampled_ = "sampled_"
    task_list = ['cycle', 'connectivity', 'bipartite', 'topology', 'shortest', 'flow', 'hamilton']
    dataset_path = 'dataset2'
    generate_size = 9
    for task_name in task_list:
        sampled_file = f"{sample_path}/{STR_sampled_}flow.json"
        sampled_tasks = utils.load_data(sampled_file)
        new_tasks = []
        for task in sampled_tasks:
            used_pairs = None
            for i in range(generate_size):
                new_task = task.copy()
                if task_name in ['cycle', 'bipartite', 'topology', 'hamilton']:
                    if i == 0:
                        new_task["removed_edge"] = None
                    else:
                        new_task, used_pairs = remove_random_edge(task, used_pairs)
                        if new_task is None:
                            break
                if task_name == 'cycle':
                    new_question = generate_cycle_question(new_task)
                elif task_name == 'bipartite':
                    new_question = generate_bipartite_question(new_task)
                elif task_name == 'topology':
                    new_question = generate_topology_sort_question(new_task)
                elif task_name == 'hamilton':
                    new_question = generate_hamiltonian_path_question(new_task)
                elif task_name == 'shortest':
                    new_question, used_pairs = generate_shortest_path_question(new_task, 2, used_pairs)
                elif task_name == 'connectivity':
                    new_question, used_pairs = generate_connectivity_question(new_task, 2, used_pairs)
                elif task_name == 'flow':
                    new_question, used_pairs = generate_max_flow_question(new_task['query'], used_pairs)
                if new_question is None:
                    continue
                new_task["query"] = new_question
                new_task["task"] = task_name
                new_tasks.append(new_task)
        output_file = f"{dataset_path}/generated_{task_name}.json"
        utils.save_data(new_tasks, output_file)
        print(f"Generated {len(new_tasks)} new tasks, saved to {output_file}")
    for task_name in task_list:
        utils.get_answer(dataset_path, task_name=task_name)
    merge_json_files(dataset_path)


def merge_json_files(dataset_path, output_file="dataset2.json"):
    output_file = os.path.join(dataset_path, output_file)
    merged_data = []
    for filename in os.listdir(dataset_path):
        if filename.endswith(".json") and filename != os.path.basename(output_file):
            file_path = os.path.join(dataset_path, filename)
            try:
                data = utils.load_data(file_path)
                merged_data.extend(data)
                print(f"Loaded file: {filename}")
            except Exception as e:
                print(f"Error loading file {filename}: {e}")
    try:
        utils.save_data(merged_data, output_file)
        print(f"Merged successfully, saved to: {output_file}")
    except Exception as e:
        print(f"Error saving merged file: {e}")


def test_cycle():
    task = {
        "query": "Determine whether or not there is a cycle in an undirected graph. In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge. Given a graph, you need to output Yes or No, indicating whether there is a cycle in the graph. Q: The nodes are numbered from 0 to 4, and the edges are: (0, 1) (1, 2) (2, 3) (3, 4). Is there a cycle in this graph?",
        "edges": [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1)]
    }
    new_query = generate_cycle_question(task)
    print(new_query)


def test_connectivity():
    task = {
        "query": "Determine whether two nodes are connected in an undirected graph. In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge. Given a graph and a pair of nodes, you need to output Yes or No, indicating whether the node i and node j are connected. Q: The nodes are numbered from 0 to 4, and the edges are: (0, 1) (1, 2) (2, 3) (3, 4). Is there a path between node 0 and node 4?",
        "edges": [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1)]
    }
    used_pairs = set()
    for _ in range(10):
        new_query, used_pairs = generate_connectivity_question(task, 2, used_pairs)
        print(new_query)
    print(f"used_pairs: {used_pairs}")


def test_bipartite():
    task = {
        "query": "Determine whether or not a graph is bipartite. In a directed graph, (i->j) means that node i and node j are connected with a directed edge from node i to node j. Given a graph, you need to output Yes or No, indicating whether the graph is bipartite. Q: The nodes are numbered from 0 to 4, and the edges are: (0->1) (1->2) (2->3) (3->4). Is this graph bipartite?",
        "edges": [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1)]
    }
    new_query = generate_bipartite_question(task)
    print(new_query)


def test_topology_sort():
    task = {
        "query": "Find one of the topology sorting paths of the given graph. In a directed graph, (i->j) means that node i and node j are connected with a directed edge from node i to node j. Given a graph, you need to output one of the topology sorting paths of the graph. Q: The nodes are numbered from 0 to 4, and the edges are: (0->1) (1->2) (2->3) (3->4). Give one topology sorting path of this graph.",
        "edges": [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1)]
    }
    new_query = generate_topology_sort_question(task)
    print(new_query)


def test_shortest_path():
    task = {
        "query": "Find the shortest path from node 0 to node 4. Q: The nodes are numbered from 0 to 4, and the edges are: (0, 1, 1) (1, 2, 1) (2, 3, 1) (3, 4, 1). Give the weight of the shortest path from node 0 to node 4.",
        "edges": [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1)]
    }
    used_pairs = set()
    for _ in range(10):
        new_query, used_pairs = generate_shortest_path_question(task, 2, used_pairs)
        print(new_query)


def test_hamiltonian_path():
    task = {
        "query": "Determine whether or not there is a Hamiltonian path in an undirected graph. In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge. Given a graph, you need to output Yes or No, indicating whether there is a Hamiltonian path in the graph. Q: The nodes are numbered from 0 to 4, and the edges are: (0, 1) (1, 2) (2, 3) (3, 4). Is there a Hamiltonian path in this graph?",
        "edges": [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1)]
    }
    new_query = generate_hamiltonian_path_question(task)
    print(new_query)


if __name__ == "__main__":
    pass
