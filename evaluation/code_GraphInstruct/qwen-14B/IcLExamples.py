import argparse
import numpy as np
import os
import torch
import json
from collections import Counter
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer
from datasets import load_dataset
from datetime import datetime
import random

# 设置环境变量，使用哪些GPU卡
os.environ['CUDA_VISIBLE_DEVICES'] = '0,1,2,3'

def apply_chat_template(toker, messages):
    input_prompt = toker.apply_chat_template(messages, add_generation_prompt=True, tokenize=False)
    return toker(input_prompt, add_special_tokens=False).input_ids

def prepare_input_with_context(template, input_d, context_examples):
    """
    准备带有上下文示例的输入
    :param input_d: 当前问题数据
    :param context_examples: 上下文示例列表 [{query, answer}, ...]
    :return: 组织好的上下文和问题
    """
    context_str = ""
    for example in context_examples:
        context_str += f"Query: {example['query']}\nAnswer: {example['answer']}\n\n"
    
    # 将目标问题添加到上下文后
    context=context_str
    #print(context)
    problem = input_d['query']
    #print(problem)


    #final_prompt = f"{context_str}{template.format(input_d['query'], '')}"
    
    prompt = template.format(context=context, problem=problem)
    #print(prompt[0])

    #print(prompt)
    
    messages = [{'role': 'user', 'content': prompt}]
    return messages

# 加载配置文件
def load_config_from_json(filename='config.json', item=None):
        with open(filename, 'r') as file:
            config = json.load(file)
            if item == 'model_path':
                return config.get('model_path', None)
            elif item == 'data_files':
                return config.get('data_files', None)
            elif item == 'template_icl':
                return config.get('template_icl', None)
            elif item == 'context_size':
                return config.get('context_size', None)
        
def main():
    model_path = load_config_from_json(item='model_path')  # 使用配置文件中的模型路径
    voting_n = 1  # 对同一个问题的回答个数
    context_size = load_config_from_json(item='context_size')  # 使用配置文件中的上下文示例数量

    # 加载 tokenizer 和模板
    toker = AutoTokenizer.from_pretrained(model_path)
    template_icl = load_config_from_json(item='template_icl')  # 使用配置文件中的模板
    template = f'/home/zch/Code/GraphICL/evaluation/templates/{template_icl}.txt'
    TEMPLATE = open(template).read().strip()   
 
    # 初始化 LLM
    llm = LLM(
        model=model_path,
        tokenizer=model_path,
        gpu_memory_utilization=0.9,
        tensor_parallel_size=4,
        enable_prefix_caching=True,
        swap_space=16,
        max_num_seqs=1024,
        trust_remote_code=True
    )
    sampling_params = SamplingParams(temperature=1, top_p=0.9, n=voting_n, max_tokens=32768, seed=42)
    # 加载数据集
    input_data = load_dataset("json", data_files=load_config_from_json(item='data_files'))  # 使用配置文件中的数据集路径

    task_types = [
    "cycle", "connectivity", "bipartite", "topology",
    "shortest", "triangle", "flow", "hamilton", "substructure"
    ]

    all_resps = []

    for task_type in task_types:
        print(f"Processing task: {task_type}")
        task_data = [item for item in input_data['train'] if item.get('task') == task_type]
        # 检查 task_data 是否为空列表
        if not task_data:
            continue
        
        # 如果上下文数量不足，使用全部示例
        if len(task_data) < context_size:
            print(f"Not enough examples for {task_type}. Reducing context size to {len(task_data)}.")
            context_size = len(task_data)
    
        prompt_token_ids = []
        resps = []
        for e in task_data:
        # 随机抽取上下文示例，排除当前问题
            filtered_examples = [item for item in task_data if item != e]
            context_examples = random.sample(filtered_examples, min(context_size, len(filtered_examples)))

            # 准备带有上下文的 prompt
            tokenized_input = prepare_input_with_context(TEMPLATE, e, context_examples)
            tokenized_prompt = apply_chat_template(toker, tokenized_input)
            prompt_token_ids.append(tokenized_prompt)
        # 调用模型生成答案
        print(f"Generating answers for task: {task_type}")
        generations = llm.generate(prompt_token_ids=prompt_token_ids, sampling_params=sampling_params)
        for i in range(len(task_data)):
            d = task_data[i].copy()
            generated = generations[i].outputs[0].text.strip()
            d['response'] = generated
            resps.append(d)
        # 将当前任务结果加入总结果
        all_resps.extend(resps)

    # 使用当前时间戳创建唯一的文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # 格式化为 YYYYMMDD_HHMMSS
    filename = f'/home/zch/Code/GraphICL/result/GraphInstruct/Qwen2.5-14B/responses_with_context_all_tasks/responses_with_context_all_tasks_{context_size}_{template_icl}_{timestamp}.json'

    with open(filename, 'w', encoding='utf8') as file:
        json.dump(all_resps, file, ensure_ascii=False, indent=4)
    
if __name__ == '__main__':
    main()
