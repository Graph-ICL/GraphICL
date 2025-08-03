import json
import random
from pathlib import Path
import os


def load_data(task_file):
    with open(task_file, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def save_data(data, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def sample_tasks(task_file, sampled_file, num_samples):
    tasks = load_data(task_file)

    if Path(sampled_file).exists():
        sampled_tasks = load_data(sampled_file)
        sampled_set = set(json.dumps(item, sort_keys=True) for item in sampled_tasks)
    else:
        sampled_set = set()

    remaining_tasks = [task for task in tasks if json.dumps(task, sort_keys=True) not in sampled_set]

    if len(remaining_tasks) < num_samples:
        raise ValueError(f"Not enough remaining samples to sample {num_samples} items. Remaining: {len(remaining_tasks)}")

    sampled = random.sample(remaining_tasks, num_samples)

    sampled_set.update(json.dumps(task, sort_keys=True) for task in sampled)
    save_data([json.loads(item) for item in sampled_set], sampled_file)

    return sampled


def run_sampling(task_file, sampled_file, sample_sizes, num_runs):
    results = []

    for size in sample_sizes:
        for run in range(num_runs):
            try:
                if size == 0:
                    sampled = []
                else:
                    sampled = sample_tasks(task_file, sampled_file, size)
                results.append({
                    "sample_size": size,
                    "run": run + 1,
                    "sampled_tasks": sampled
                })
                print(f"Sampled {size} items, run {run + 1} completed")
            except ValueError as e:
                print(e)
                break

    save_data(results, f"{sample_path}/{task_name}_sampling_results.json")
    print(f"All sampling results saved to {sample_path}/{task_name}_sampling_results.json")


def get_sampled_result(task_name):
    task_file = f"{task_path}/{task_name}.json"
    sampled_file = f"{sample_path}/sampled_{task_name}.json"
    sample_sizes = [1, 2, 4, 8]
    num_runs = 8
    run_sampling(task_file, sampled_file, sample_sizes, num_runs)


task_path = "task-list"
sample_path = "sampled-list"
os.makedirs(sample_path, exist_ok=True)
task_name = "cycle"
get_sampled_result(task_name)
