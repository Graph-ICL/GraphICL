# GraphICL

## 项目描述

本项目旨在探索和评估大语言模型（LLM）在图上下文学习任务中的表现。通过设计一系列实验，我们测试了模型在处理图问题时的上下文推理能力。实验代码包含测试的框架、自定义图数据集、模型配置和评估指标。

## 安装要求

### 环境要求

- **操作系统**：Linux
- **Python**：3.8+

### 安装步骤

1. 克隆项目到本地：
    ```bash
    git clone https://github.com/GraphICL/GraphICL.git
    cd GraphICL
    ```

2. 安装依赖：
    ```bash
    pip install -r o1.txt
    npm install
    ```

## 项目特点

- **针对图上下文的专项测试**：
本项目专注于评估大语言模型在处理问题时的上下文理解与推理能力，填补了大模型在图相关任务中的评测空白。


## 基本结构
    GraphICL/
    ├── data/                   # 数据目录，存放实验所需的数据集
    ├── evaluation/             #代码目录，包含测试代码和结果分析工具
    │   ├── code_GraphInstruct/     # GraphInstruct 数据集测试相关代码
    │   ├── code_GraphSCR/          # GraphSCR 数据集测试相关代码
    │   ├── code_GraphTRB/          # GraphTRB 数据集测试相关代码
    │   └── templates/              # 模板文件，用于构建大模型输入
    ├── generate_dataset/       # 数据集生成代码
    ├── result/                 # 实验结果目录，存放实验输出结果
    │   ├── GraphInstruct/          # GraphInstruct 数据集输出结果
    │   ├── GraphSCR/               # GraphSCR 数据集输出结果
    │   └── GraphTRB/               # GraphTRB 数据集输出结果
    ├── environments.yml        # 环境配置文件，用于设置实验环境
    ├── o1.txt                 # 项目依赖文档
    └── README.md              # 项目说明文档

## 使用方法

- **命令行**：
    （以GraphInstruct数据集的qwen-7B模型测试为例）
    - 切换目录：
        ```bash
        cd Code/GraphICL/evaluation/code_GraphInstruct/qwen-7B
        ```
    - 修改配置参数：
        ```bash
        {
            "model_path": "/home/zch/Code/model/Qwen2.5-7B/Qwen/Qwen2___5-7B-Instruct",     # 模型路径
            "data_files": "/home/zch/Code/GraphICL/data/GraphInstruct.json",        # 数据集路径
            "template": "query_template2",      # 使用模板
            "template_icl": "query_template_icl2",      # 使用模板
            "context_size": 8,     # 上下文示例数量
            "result_file": "test1"      # 要进行准确率评估的测试结果文件标识
        }
        ```
    - 启动项目：
        ```bash
        python IclAbilityTest.py            # 无上下文用例结果生成
        python IclAbilityTestResults.py     # 无上下文用例结果准确率评估
        python IcLExamples.py               # 有上下文用例结果生成
        python IclExamplesTestResults.py    # 有上下文用例结果准确率评估
        ```
    - 生成结果：
        结果生成在Code/GraphICL/result/GraphInstruct/qwen-7B中，可自行修改结果生成目录路径，结果各文件夹如下：
        - responses：无上下文用例结果
        - task_accuracies：无上下文用例结果准确率
        - responses_with_context_all_tasks：有上下文用例结果
        - ICLtask_accuracies：有上下文用例结果准确率
    - 具体步骤：
        1. 修改配置参数，运行有/无上下文用例结果生成程序文件
        2. 在result文件夹下找到有/无上下文用例结果文件，确定文件标识
        3. 修改配置参数文件中的要进行准确率评估的测试结果文件标识，运行有/无上下文用例结果准确率评估程序文件
        4. 在result文件夹下找到所得到的结果准确率文件

## 附录

### 数据集GraphSCB

| 同类 `task` | 同个图 | 不同的问题 |
| ----------- | ------ | ---------- |


 `connectivity`,`shortest`, `flow` 
1. - 根据结点数不同，分为不同难度
     `easy: [5,35]; middle: (35,65], hard: (65,100]` ,
     即`easy: [5,36); middle: [36,66), hard: [66,101)` 
   - 图的数量尽量抽取 100 个，若难度范围内没有 100 个图，则全部抽取
   
   - 建立主键 `"graph"`，和键 `"complexity"`
   
2. 为每个问题生成同类别问题 ==16== 个


3. 答案格式使用 `###` 作为前缀符
   eg：`### Yes` 或 `### No`

> [example]
>
> 数据集的 `json` 格式：
>
> ```json
> {
>     "query":{},
>     "answer":{},
>     "task":{},		// connectivity, shortest, flow
>     "graph":{},    // graph<num>
>     "complexity":{}      // easy, middle, hard   
> }
> ```
>

对应文件 `GraphSCB.json`

### 数据集GraphTRB

| 不同类 `task` | 同个图 | 不同的问题 |
| ------------- | ------ | ---------- |


> [example]
>
> 数据集的 `json` 格式：
>
> ```json
> {
>     "query":{},
>     "answer":{},
>     "task":{},
>     "graph":{}
> }
> ```

| cycle  | connect | bipartite | topology                             |
| ------ | ------- | --------- | ------------------------------------ |
| Yes/No | Yes/No  | Yes/No    | topology sorting path<br />eg. [ , ] |

| shortest                               | triangle                                                     | flow                                              | hamilton | subgraph |
| -------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------- | -------- | -------- |
| weight of the shortest path<br />(num) | maximum sum of the weights of three interconnected nodes<br />(num) | the maximum flow between the two nodes<br />(num) | Yes/No   | Yes/No   |

对应文件 `GraphTRB.json`
