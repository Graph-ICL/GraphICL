import json
from collections import defaultdict
import os

# 输入文件路径
input_file = "GraphInstruct.json"

# 按任务分类的字典
task_to_data = defaultdict(list)

# 逐行读取 JSON 文件
with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():  # 跳过空行
            # 解析每行的 JSON 对象
            item = json.loads(line.strip())
            # 获取任务类型
            task = item["task"]
            # 将数据添加到对应任务的列表中
            task_to_data[task].append(item)

# 创建存储 JSON 文件夹
folder_path = "task-list"
os.makedirs(folder_path, exist_ok=True)


# 将分类后的数据保存到对应的 JSON 文件
for task, items in task_to_data.items():
    output_file = f"{folder_path}\{task}.json"  # 根据任务名称生成输出文件名
    with open(output_file, "w", encoding="utf-8") as f:
        # 将数据保存为 JSON 文件（每行一个 JSON 对象）
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"Saved {len(items)} items to {output_file}")