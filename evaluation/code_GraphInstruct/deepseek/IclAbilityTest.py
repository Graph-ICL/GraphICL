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
import re

# 设置环境变量，使用哪些GPU卡
os.environ['CUDA_VISIBLE_DEVICES'] = '4,5,6,7'

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
    prompt = template.format(problem=problem)
    messages = [{'role': 'user', 'content': prompt}]
    return messages

# 加载配置文件
def load_config_from_json(filename='config.json', item=None):
        with open(filename, 'r') as file:
            config = json.load(file)
            if item == 'model_path':
                return config.get('model_path1', None)
            elif item == 'data_files':
                return config.get('data_files', None)
            elif item == 'template':
                return config.get('template', None)
        
def main():
    model_path = load_config_from_json(item='model_path')  # 使用配置文件中的模型路径
    voting_n = 1  # 对同一个问题的回答个数

    # 加载 tokenizer 和模板
    toker = AutoTokenizer.from_pretrained(model_path)
    template_name = load_config_from_json(item='template')  # 使用配置文件中的模板
    template = f'/home/zch/Code/GraphICL/evaluation/templates/{template_name}.txt'
    TEMPLATE = open(template).read().strip()   

    # 初始化 LLM
    llm = LLM(
        model=model_path,
        tokenizer=model_path,
        gpu_memory_utilization=0.85,
        tensor_parallel_size=4,
        enable_prefix_caching=True,
        swap_space=16,
        max_num_seqs=1024,
    )
    sampling_params = SamplingParams(temperature=1, top_p=0.9, n=voting_n, max_tokens=8192, seed=42)

    # 加载数据集
    input_data = load_dataset("json", data_files=load_config_from_json(item='data_files'))  # 使用配置文件中的数据集路径

    prompt_token_ids = []
    for e in input_data['train']:
        tokenized_input = prepare_input_boxed(TEMPLATE, e)
        tokenized_prompt = apply_chat_template(toker, tokenized_input)
        prompt_token_ids.append(tokenized_prompt)

    print(len(prompt_token_ids))
    generations = llm.generate(prompt_token_ids=prompt_token_ids, sampling_params=sampling_params)
    resps = []

    for i in range(len(input_data['train'])):
     # 复制，添加新字段
       d = input_data['train'][i].copy()
       generated = generations[i].outputs[0].text
       d['response'] = generated
       resps.append(d)

    # 使用当前时间戳创建唯一的文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # 格式化为 YYYYMMDD_HHMMSS
    filename = f'/home/zch/Code/GraphICL/result/GraphInstruct/DeepSeek/test3/responses/responses_{template_name}_{timestamp}.json'

    with open(filename, 'w', encoding='utf8') as file:
        json.dump(resps, file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()