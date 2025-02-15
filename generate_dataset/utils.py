import json
import random
from pathlib import Path
import os
import graph_algo
from tqdm import tqdm

def load_data(task_file):
    """从 JSON 文件中加载任务数据"""
    with open(task_file, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def save_data(data, output_file):
    """将数据保存到 JSON 文件"""
    with open(output_file, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")



import os
import json
import random
from pathlib import Path
from utils import load_data, save_data
from graph_algo import extract_node_num


def sample_tasks(task_file, sampled_file, num_samples, node_num_min, node_num_max):
    """
    对某类任务进行采样，确保与之前的样本不重复，并且只采样节点数在 [node_num_min, node_num_max] 范围内的任务。
    如果已经采样过会继续采样，并且保证不与之前的样本重复。
    如果剩余样本不足，继续执行并提醒实际采样的数量。
    根据节点数范围添加 "complexity" 键值对：
        - easy: [5, 35]
        - middle: (35, 65]
        - hard: (65, 100]
    :param task_file: 分类后的任务文件路径
    :param sampled_file: 已采样的样本文件路径
    :param num_samples: 需要采样的条数
    :param node_num_min: 节点数最小值（包含）
    :param node_num_max: 节点数最大值（包含）
    :return: 实际采样的任务列表
    """
    # 加载任务数据
    tasks = load_data(task_file)

    # 加载已采样的样本
    if Path(sampled_file).exists():
        sampled_tasks = load_data(sampled_file)
        # 使用 graph 字段作为主键
        sampled_set = {item["graph"]: item for item in sampled_tasks}
    else:
        sampled_set = {}

    # 过滤掉已采样的样本
    remaining_tasks = []
    for task in tasks:
        task_json = json.dumps(task, sort_keys=True)
        # 检查任务是否已被采样
        if task_json not in [json.dumps(item, sort_keys=True) for item in sampled_set.values()]:
            remaining_tasks.append(task)

    # 进一步筛选节点数在 [node_num_min, node_num_max] 范围内的任务
    filtered_tasks = [
        task for task in remaining_tasks
        if node_num_min <= extract_node_num(task["query"]) <= node_num_max
    ]

    # 检查剩余样本是否足够
    if len(filtered_tasks) < num_samples:
        print(
            f"警告：剩余样本不足，无法采样 {num_samples} 条。"
            f"剩余样本数：{len(filtered_tasks)}，节点数范围：[{node_num_min}, {node_num_max}]"
        )
        num_samples = len(filtered_tasks)  # 调整采样数量为剩余样本数

    # 随机采样
    sampled = random.sample(filtered_tasks, num_samples)

    # 为采样的任务添加主键和 complexity 字段  (这里可以优化下，有点慢)
    for i, task in enumerate(sampled, start=len(sampled_set) + 1):
        task["graph"] = f"graph{i}"  # 添加主键

        # 根据节点数范围设置 complexity
        node_num = extract_node_num(task["query"])
        if 5 <= node_num <= 35:
            task["complexity"] = "easy"
        elif 35 < node_num <= 65:
            task["complexity"] = "middle"
        elif 65 < node_num <= 100:
            task["complexity"] = "hard"
        else:
            task["complexity"] = "unknown"  # 默认值，防止意外情况

        sampled_set[task["graph"]] = task  # 更新已采样的样本记录

    # 保存已采样的样本记录
    save_data(list(sampled_set.values()), sampled_file)
    print(
        f"已采样 {len(sampled)} 条任务，保存到 {sampled_file}，"
        f"节点数范围：[{node_num_min}, {node_num_max}]"
    )

    return sampled

def get_answer(task_path, task_name):
    """
    根据不同算法计算生成任务的答案并且替换原答案
    :param task_path: 任务文件路径
    :param task_name: 任务名称
    """
    task_file = f"{task_path}\generated_{task_name}.json"  # 分类后的任务文件
    tasks = load_data(task_file)
    total_questions = len(tasks)
    print(f"总问题数: {total_questions}")

    # 使用 tqdm 包裹循环
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
    print(f"任务 {task_name} 的答案已更新并保存到 {task_file}")

def extract_graph(sampled_file):
    """
    为采样出的 flow 任务提取图结构
    然后为每个图数据添加一个 edges 字段存储图结构
    :param sampled_file: 采样文件路径
    """

    # 加载任务数据
    tasks = load_data(sampled_file)

    # 使用 tqdm 包裹循环
    for i, task in enumerate(tqdm(tasks, desc="Extracting graph edges"), start=1):
        query = task['query']
        edges = graph_algo.extract_edges_d(query)
        task['edges'] = edges

    # 保存包含图结构的任务数据
    save_data(tasks, sampled_file)
    print(f"图结构已提取并保存到 {sampled_file}")


def sample_dataset1():
    """
    采样 dataset1 中的任务
    """

    # 示例调用
    task_path = "task-list"
    sample_path = "sampled-dataset1"
    os.makedirs(sample_path, exist_ok=True)
    # task_name = "cycle"
    task_list = ['connectivity', 'flow', 'shortest']
    for task_name in task_list:
        task_file = f"{task_path}\{task_name}.json"  # 分类后的任务文件
        sampled_file = f"{sample_path}\sampled_{task_name}.json"  # 已采样的样本文件
        num_samples = 100  # 需要采样的条数
        sample_tasks(task_file, sampled_file, num_samples, 5, 35)
        sample_tasks(task_file, sampled_file, num_samples, 36, 65)
        sample_tasks(task_file, sampled_file, num_samples, 65, 100)


def sample_dataset2():
    # 示例调用
    task_path = "task-list"
    sample_path = "sampled-dataset2"
    os.makedirs(sample_path, exist_ok=True)
    task_name = "flow"
    task_file = f"{task_path}\{task_name}.json"  # 分类后的任务文件
    sampled_file = f"{sample_path}\sampled_{task_name}.json"  # 已采样的样本文件
    num_samples = 100  # 需要采样的条数
    sample_tasks(task_file, sampled_file, num_samples, 10, 20)
    extract_graph(sampled_file)

    

if __name__ == '__main__':
    sample_dataset2()