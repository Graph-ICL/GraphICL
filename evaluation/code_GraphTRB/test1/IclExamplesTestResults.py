import argparse
import numpy as np
import os
import torch
import json
from collections import Counter
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer
from datasets import load_dataset
import re

# 设置环境变量，使用哪些GPU卡
os.environ['CUDA_VISIBLE_DEVICES'] = '0,1,2,3'

def apply_chat_template(toker, messages):
    input_prompt = toker.apply_chat_template(messages, add_generation_prompt=True, tokenize=False)
    return toker(input_prompt, add_special_tokens=False).input_ids

def prepare_input_boxed(template, input_d):
    """
        critique_template.txt
        包含problem和tagged_response两个待填入字段
    """
    #print(input_d)
    problem = input_d['query']
    solution = input_d['answer']
    response= input_d['response']

    prompt = template.format(problem=problem, solution=solution, response=response)
    messages = [{'role': 'user', 'content': prompt}]
    return messages

# 加载配置文件
def load_config_from_json(filename='config.json', item=None):
        with open(filename, 'r') as file:
            config = json.load(file)
            if item == 'model_path':
                return config.get('model_path', None)
            elif item == 'result_file':
                return config.get('result_file', None)
            
def main():
    model_path = load_config_from_json(item='model_path')  # 使用配置文件中的模型路径
    voting_n = 1  # 对同一个问题的回答个数

    # 加载 tokenizer 和模板
    toker = AutoTokenizer.from_pretrained(model_path)

    TEMPLATE = open('/home/zch/Code/GraphICL/evaluation/templates/judge_template.txt').read().strip()
    # 初始化 LLM
    llm = LLM(
        model=model_path,
        tokenizer=model_path,
        gpu_memory_utilization=0.8,
        tensor_parallel_size=4,
        enable_prefix_caching=True,
        swap_space=16,
        max_num_seqs=1024,
    )
    sampling_params = SamplingParams(temperature=1, top_p=0.9, n=voting_n, max_tokens=8192, seed=42)

    result_file = load_config_from_json(item='result_file')  # 使用配置文件中的测试结果文件标识

    # 构建文件路径
    file_path1 = f"/home/zch/Code/GraphICL/result/GraphTRB/responses_with_context_all_tasks/responses_with_context_all_tasks_{result_file}.json"

    # 加载特定的数据集
    input_data = load_dataset("json", data_files=file_path1)
    #import ipdb; ipdb.set_trace()

    #按照 task 分类
    task_groups = {}
    for item in input_data['train']:
        task = (item['task'], item['category'])
        if task not in task_groups:
            task_groups[task] = []
        task_groups[task].append(item)

    # 构建文件路径
    file_path2 = f'/home/zch/Code/GraphICL/result/GraphTRB/ICLtask_accuracies/ICLtask_accuracies_{result_file}.txt'

    # 打开文件用于写入任务准确率
    with open(file_path2, 'w') as accuracy_file:
        # 对每个 task 分类进行准确率计算
        task_accuracies = {}
        for task, task_data in task_groups.items():
            print(f"Evaluating task: {task}")

            # 生成每个问题的 prompt
            prompt_token_ids = [apply_chat_template(toker, prepare_input_boxed(TEMPLATE, e)) for e in task_data]

            # 批量生成回答
            generations = llm.generate(prompt_token_ids=prompt_token_ids, sampling_params=sampling_params)

            correct_count = 0  # 记录正确的回答个数

            # 对每个问题，获取模型生成的回答并与正确答案对比
            for i in range(len(task_data)):
                if voting_n == 1:
                    generated_critique = generations[i].outputs[0].text
                else:
                    generated_critique = [ee.text for ee in generations[i].outputs]

                
                # 比较最终答案是否一致
                if generated_critique == "Yes":
                    correct_count += 1  # 如果答案一致，计数正确

            # 计算并存储该任务的准确率
            accuracy = correct_count / len(task_data) if len(task_data) > 0 else 0
            task_accuracies[task] = accuracy

            # 将任务和准确率写入文件
            accuracy_file.write(f"Accuracy for task '{task}': {accuracy * 100:.2f}%\n")
            #break

        # 输出所有任务的准确率到文件
        accuracy_file.write("\nOverall accuracy per task:\n")
        for task, accuracy in task_accuracies.items():
            accuracy_file.write(f"Task: {task}, Accuracy: {accuracy * 100:.2f}%\n")

    print("Accuracy data has been saved to 'task_accuracies.txt'.")

if __name__ == '__main__':
    main()