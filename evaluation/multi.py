```python
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


def apply_chat_template(toker, messages):
    input_prompt = toker.apply_chat_template(messages, add_generation_prompt=True, tokenize=False)
    return toker(input_prompt, add_special_tokens=False).input_ids


def prepare_input_boxed(template, input_d):
    problem = input_d['problem']
    steps = input_d['steps']
    tagged_response = ''
    for sdx, step in enumerate(steps):
        tagged_response += f'<paragraph_{sdx}>\n{step}\n</paragraph_{sdx}>\n\n'
    tagged_response = tagged_response.strip()
    prompt = template.format(problem=problem, tagged_response=tagged_response)
    messages = [{'role': 'user', 'content': prompt}]
    return messages


def main():
    model_path = '/home/fujiarun/lihao/Qwen2.5-3B-Instruct/Qwen/Qwen2___5-3B-Instruct'
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

    input_data = load_dataset("json", data_files="../processData/gsm8k_updated.json")

    prompt_token_ids = [apply_chat_template(toker, prepare_input_boxed(TEMPLATE, e)) for e in input_data]

    generations = llm.generate(prompt_token_ids=prompt_token_ids, sampling_params=sampling_params)

    res_data = []
    for i in range(len(input_data)):
        if voting_n == 1:
            generated_critique = generations[i].outputs[0].text
        else:
            generated_critique = [ee.text for ee in generations[i].outputs]
        res_data.append(generated_critique)
    print(res_data)


if __name__ == '__main__':
    main()
```
