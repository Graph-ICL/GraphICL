import os
import json
from collections import defaultdict
import matplotlib.pyplot as plt
from utils import load_data
from graph_algo import extract_node_num


def count_tasks_by_node_range(task_dir, node_ranges):
    task_files = os.listdir(task_dir)
    task_stats = defaultdict(lambda: defaultdict(int))

    for task_file in task_files:
        if task_file.endswith('.json'):
            task_name = task_file.split('.')[0]
            task_path = os.path.join(task_dir, task_file)
            print(f"Processing {task_path}...")
            data = load_data(task_path)

            for item in data:
                query = item.get('query', {})
                node_num = extract_node_num(query)

                for range_start, range_end in node_ranges:
                    if range_start <= node_num < range_end:
                        task_stats[task_name][(range_start, range_end)] += 1
                        break

    return task_stats

def plot_task_stats(task_stats, node_ranges):
    # 定义颜色和标记样式
    colors = plt.cm.tab10.colors

    for task_name, stats in task_stats.items():
        plt.figure(figsize=(10, 6))  # 每个任务单独一个图
        x = [f"[{r[0]}-{r[1]})" for r in node_ranges]
        y = [stats.get(r, 0) for r in node_ranges]

        # 绘制柱状图
        bars = plt.bar(x, y, color=colors[0], label=task_name)

        # 在每个柱子上标注数量
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,  # X 坐标：柱子中心
                height + 0.5,  # Y 坐标：柱子顶部稍微上方
                f'{int(height)}',  # 标注的文本
                ha='center',  # 水平居中
                va='bottom'  # 垂直对齐到柱子顶部
            )

        plt.xlabel('Node Range')
        plt.ylabel('Number of Tasks')
        plt.title(f'Task Distribution by Node Range: {task_name}')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

def main():
    task_dir = 'task-list'
    # node_ranges = [(0, 10), (10, 20), (20, 30), (30, 40), (40, 50), (50, 60), (60, 70), (70, 80), (80, 90), (90, 100)]
    node_ranges = [(5, 36), (36, 66), (66, 101)]

    # 统计任务个数
    task_stats = count_tasks_by_node_range(task_dir, node_ranges)

    # 打印统计结果
    for task_name, stats in task_stats.items():
        print(f"Task: {task_name}") 
        for range_start, range_end in node_ranges:
            count = stats.get((range_start, range_end), 0)
            print(f"  Nodes [{range_start}:{range_end}): {count} tasks")
        print()

    # 绘制图表
    plot_task_stats(task_stats, node_ranges)

if __name__ == "__main__":
    main()