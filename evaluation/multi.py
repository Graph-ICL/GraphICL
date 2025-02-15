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
# 可以在运行前看哪些卡还有空余
# os.environ['CUDA_VISIBLE_DEVICES'] = '4,5,6,7'

def apply_chat_template(toker, messages):
    input_prompt = toker.apply_chat_template(messages, add_generation_prompt=True, tokenize=False)
    return toker(input_prompt, add_special_tokens=False).input_ids

def prepare_input_boxed(template, input_d):
    # 这个函数生成了message，也就是说这个函数需要根据实际情况修改
    """
        critique_template.txt
        包含problem和tagged_response两个待填入字段
    """
    # 这几行是根据实际情况的预处理
    problem = input_d['problem']
    steps = input_d['steps']
    tagged_response = ''
    for sdx, step in enumerate(steps):
        tagged_response += f'<paragraph_{sdx}>\n{step}\n</paragraph_{sdx}>\n\n'
    tagged_response = tagged_response.strip()
    
    # 根据template生成对应的prompt，缺哪个字段，用参数填哪个字段
    prompt = template.format(problem=problem, tagged_response=tagged_response)
    messages = [{'role': 'user', 'content': prompt}]
    return messages

def main():
    
    # 模型路径
    model_path = '/home/fujiarun/lihao/Qwen2.5-3B-Instruct/Qwen/Qwen2___5-3B-Instruct'
    # 对同一个问题的回答个数
    voting_n = 1
    
    toker = AutoTokenizer.from_pretrained(model_path)
    TEMPLATE = open('./templates/critique_template.txt').read().strip()

    llm = LLM(
        model=model_path, 
        tokenizer=model_path,
        gpu_memory_utilization=0.95,
        tensor_parallel_size=torch.cuda.device_count(),
        enable_prefix_caching=True, 
        swap_space=16,
        max_num_seqs=20,
    )
    sampling_params = SamplingParams(temperature=1, top_p=0.9, n=voting_n, max_tokens=8192, seed=42)
    
    # 导入本地数据集
    input_data = load_dataset("json", data_files="../processData/gsm8k_updated.json")
    
    # 导入非本地数据集
    # input_data = load_dataset('YorickHe/alpaca_data', split='train')
    
    # 生成本地数据集的问题列表
    # 这里的e是一个完整的json数据
    prompt_token_ids = [apply_chat_template(toker, prepare_input_boxed(TEMPLATE, e)) for e in input_data]
    
    # 生成非本地数据集的问题列表
    # prompt_token_ids = [apply_chat_template(toker, prepare_input_boxed(TEMPLATE, e)) for e in input_data]
    
    # 批量生成回答
    generations = llm.generate(prompt_token_ids=prompt_token_ids, sampling_params=sampling_params)

    res_data = []
    # 根据输入数据，从所有结果中拿对应回答
    for i in range(len(input_data)):
        if voting_n == 1:
            generated_critique = generations[i].outputs[0].text
        else:
            generated_critique = [ee.text for ee in generations[i].outputs]
        res_data.append(generated_critique)
    print(res_data)
    
    # 对拿到的结果进一步处理代码也根据实际情况继续编写

if __name__ == '__main__':
    main()
