import json
import random
from pathlib import Path
import os

def load_data(task_file):
    """从 JSON 文件中加载任务数据"""
    with open(task_file, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def save_data(data, output_file):
    """将数据保存到 JSON 文件"""
    with open(output_file, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

def sample_tasks(task_file, sampled_file, num_samples):
    """
    对某类任务进行采样，确保与之前的样本不重复
    :param task_file: 分类后的任务文件路径
    :param sampled_file: 已采样的样本文件路径
    :param num_samples: 需要采样的条数
    :return: 采样结果（列表）
    """
    # 加载任务数据
    tasks = load_data(task_file)

    # 加载已采样的样本
    if Path(sampled_file).exists():
        sampled_tasks = load_data(sampled_file)
        sampled_set = set(json.dumps(item, sort_keys=True) for item in sampled_tasks)
    else:
        sampled_set = set()

    # 过滤掉已采样的样本
    remaining_tasks = [task for task in tasks if json.dumps(task, sort_keys=True) not in sampled_set]

    # 检查剩余样本是否足够
    if len(remaining_tasks) < num_samples:
        raise ValueError(f"剩余样本不足，无法采样 {num_samples} 条。剩余样本数：{len(remaining_tasks)}")

    # 随机采样
    sampled = random.sample(remaining_tasks, num_samples)

    # 更新已采样的样本记录
    sampled_set.update(json.dumps(task, sort_keys=True) for task in sampled)
    save_data([json.loads(item) for item in sampled_set], sampled_file)

    return sampled

def run_sampling(task_file, sampled_file, sample_sizes, num_runs):
    """
    对每类任务进行多次采样
    :param task_file: 分类后的任务文件路径
    :param sampled_file: 已采样的样本文件路径
    :param sample_sizes: 采样条数列表（如 [0, 2, 4, 8]）
    :param num_runs: 每种条数的采样次数
    """
    results = []

    for size in sample_sizes:
        for run in range(num_runs):
            try:
                if size == 0:
                    # 采样 0 条，直接跳过
                    sampled = []
                else:
                    # 采样指定条数
                    sampled = sample_tasks(task_file, sampled_file, size)
                results.append({
                    "sample_size": size,
                    "run": run + 1,
                    "sampled_tasks": sampled
                })
                print(f"采样条数: {size}, 第 {run + 1} 次采样完成")
            except ValueError as e:
                print(e)
                break

    # 保存所有采样结果
    save_data(results, f"{sample_path}\{task_name}_sampling_results.json")
    print(f"所有采样结果已保存到 {sample_path}\{task_name}_sampling_results.json")

def get_sampled_result(task_name):
    """
    获取某类任务的采样结果
    :param task_name: 任务名称
    """
    task_file = f"{task_path}\{task_name}.json"  # 分类后的任务文件
    sampled_file = f"{sample_path}\sampled_{task_name}.json"  # 已采样的样本文件
    sample_sizes = [1, 2, 4, 8]  # 采样条数
    num_runs = 8  # 每种条数的采样次数
    run_sampling(task_file, sampled_file, sample_sizes, num_runs)


# 示例调用
task_path = "task-list"
sample_path = "sampled-list"
os.makedirs(sample_path, exist_ok=True)
task_name = "cycle"
get_sampled_result(task_name)





