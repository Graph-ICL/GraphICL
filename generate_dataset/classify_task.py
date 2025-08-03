import json
from collections import defaultdict
import os

input_file = "GraphInstruct.json"

task_to_data = defaultdict(list)

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            item = json.loads(line.strip())
            task = item["task"]
            task_to_data[task].append(item)

folder_path = "task-list"
os.makedirs(folder_path, exist_ok=True)

for task, items in task_to_data.items():
    output_file = f"{folder_path}/{task}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"Saved {len(items)} items to {output_file}")
