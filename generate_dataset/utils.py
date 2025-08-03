import json
import random
from pathlib import Path
import os
import graph_algo
from tqdm import tqdm


def load_data(task_file):
    with open(task_file, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def save_data(data, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def sample_tasks(task_file, sampled_file, num_samples, node_num_min, node_num_max):
    tasks = load_data(task_file)

    if Path(sampled_file).exists():
        sampled_tasks = load_data(sampled_file)
        sampled_set = {item["graph"]: item for item in sampled_tasks}
    else:
        sampled_set = {}

    remaining_tasks = []
    for task in tasks:
        task_json = json.dumps(task, sort_keys=True)
        if task_json not in [json.dumps(item, sort_keys=True) for item in sampled_set.values()]:
            remaining_tasks.append(task)

    filtered_tasks = [
        task for task in remaining_tasks
        if node_num_min <= graph_algo.extract_node_num(task["query"]) <= node_num_max
    ]

    if len(filtered_tasks) < num_samples:
        print(
            f"Warning: Not enough remaining samples. Available: {len(filtered_tasks)}, "
            f"Required: {num_samples}. Sampling all available."
        )
        num_samples = len(filtered_tasks)

    sampled = random.sample(filtered_tasks, num_samples)

    for i, task in enumerate(sampled, start=len(sampled_set) + 1):
        task["graph"] = f"graph{i}"

        node_num = graph_algo.extract_node_num(task["query"])
        if 5 <= node_num <= 35:
            task["complexity"] = "easy"
        elif 35 < node_num <= 65:
            task["complexity"] = "middle"
        elif 65 < node_num <= 100:
            task["complexity"] = "hard"
        else:
            task["complexity"] = "unknown"

        sampled_set[task["graph"]] = task

    save_data(list(sampled_set.values()), sampled_file)
    print(
        f"Sampled {len(sampled)} tasks to {sampled_file}, "
        f"node range: [{node_num_min}, {node_num_max}]"
    )

    return sampled


def get_answer(task_path, task_name):
    task_file = f"{task_path}/generated_{task_name}.json"
    tasks = load_data(task_file)
    total_questions = len(tasks)
    print(f"Total questions: {total_questions}")

    for i, task in enumerate(tqdm(tasks, desc=f"Answering {task_name}"), start=1):
        query = task['query']
        if task_name == 'cycle':
            edges = graph_algo.extract_edges_a(query)
            result = graph_algo.has_cycle(edges)
        elif task_name == 'connectivity':
            edges = graph_algo.extract_edges_a(query)
            node1, node2 = graph_algo.extract_nodes(query)
            result = graph_algo.are_nodes_connected(edges, node1, node2)
        elif task_name == 'bipartite':
            edges = graph_algo.extract_edges_b(query)
            result = graph_algo.is_bipartite(edges)
        elif task_name == 'topology':
            edges = graph_algo.extract_edges_b(query)
            result = graph_algo.topological_sort(edges)
        elif task_name == 'shortest':
            edges = graph_algo.extract_edges_c(query)
            node1, node2 = graph_algo.extract_nodes(query)
            result = graph_algo.shortest_path_weight(edges, node1, node2)
        elif task_name == 'triangle':
            edges = graph_algo.extract_edges_a(query)
            node_weights = graph_algo.extract_node_weights(query)
            result = graph_algo.max_weight_of_triangle(node_weights, edges)
        elif task_name == 'flow':
            edges = graph_algo.extract_edges_d(query)
            source, target = graph_algo.extract_nodes(query)
            result = graph_algo.max_flow(edges, source, target)
        elif task_name == 'hamilton':
            edges = graph_algo.extract_edges_a(query)
            num_nodes = graph_algo.extract_node_num(query)
            result = graph_algo.has_hamiltonian_path(edges, num_nodes)
        elif task_name == 'substructure':
            edges1, edges2 = graph_algo.extract_edges_subgraph(query)
            result = graph_algo.is_subgraph(edges1, edges2)
        task['answer'] = result

    save_data(tasks, task_file)
    print(f"Answers for {task_name} saved to {task_file}")


def extract_graph(sampled_file):
    tasks = load_data(sampled_file)

    for i, task in enumerate(tqdm(tasks, desc="Extracting graph edges"), start=1):
        query = task['query']
        edges = graph_algo.extract_edges_d(query)
        task['edges'] = edges

    save_data(tasks, sampled_file)
    print(f"Graph edges extracted and saved to {sampled_file}")


def sample_dataset1():
    task_path = "task-list"
    sample_path = "sampled-dataset1"
    os.makedirs(sample_path, exist_ok=True)
    task_list = ['connectivity', 'flow', 'shortest']
    for task_name in task_list:
        task_file = f"{task_path}/{task_name}.json"
        sampled_file = f"{sample_path}/sampled_{task_name}.json"
        num_samples = 100
        sample_tasks(task_file, sampled_file, num_samples, 5, 35)
        sample_tasks(task_file, sampled_file, num_samples, 36, 65)
        sample_tasks(task_file, sampled_file, num_samples, 65, 100)


def sample_dataset2():
    task_path = "task-list"
    sample_path = "sampled-dataset2"
    os.makedirs(sample_path, exist_ok=True)
    task_name = "flow"
    task_file = f"{task_path}/{task_name}.json"
    sampled_file = f"{sample_path}/sampled_{task_name}.json"
    num_samples = 100
    sample_tasks(task_file, sampled_file, num_samples, 10, 20)
    extract_graph(sampled_file)


if __name__ == '__main__':
    sample_dataset2()
