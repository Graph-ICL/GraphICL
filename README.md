# GraphICL

## Project description

This project aims to explore and evaluate the performance of LLM on graph context learning tasks. By designing a series of experiments, we test the contextual reasoning ability of the model when dealing with graph problems. The experimental code contains the tested framework, custom graph datasets, model configurations, and evaluation metrics.

## Installation requirements

### Environmental requirements

- **Operating system**:Linux
- **Python**:3.8+

### Installation steps

1. Clone the project locally:
    ```bash
    git clone https://github.com/GraphICL/GraphICL.git
    cd GraphICL
    ```

2. Installing dependencies:
    ```bash
    pip install -r o1.txt
    npm install
    ```

## Project features

- **Specific tests for the graph context**:
This project focuses on evaluating the contextual understanding and reasoning ability of large language models in dealing with problems, filling the gap in the evaluation of large models in graph-related tasks.

- **Flexible experimental framework**:
It provides highly configurable experimental Settings, supports custom graph datasets, model types, etc., and facilitates researchers to quickly adjust experimental designs according to their needs.

- **Multi-dimensional evaluation system**:
A variety of test tasks (such as the same task for the same graph, different tasks for the same graph, etc.) are designed to comprehensively evaluate the performance of the model in different graph context scenarios.

- **Modular design**:
The code is clearly structured, and the modular design makes it easy and fast to scale to new tasks, models, or datasets.

- **Cross-platform compatibility**:
It supports running in multiple environments (e.g., local machine, cloud server), and is compatible with mainstream large model frameworks (e.g., qwen, llama, etc.).

- **Open source and reproducibility**:
The project is completely open source and provides detailed documentation and sample code to ensure reproducibility and transparency of experiments.

## Basic structure
    GraphICL/
    ├── data/                   # Data directory, where the datasets needed for the experiment are stored
    ├── evaluation/             #Code directory containing test code and result analysis tools
    │   ├── code_GraphInstruct/     # Testing code on the GraphInstruct dataset
    │   ├── code_GraphSCR/          # Testing code on the GraphSCR dataset
    │   ├── code_GraphTRB/          # Testing code on the GraphTRB dataset
    │   └── templates/              # Template files, used to build LLM inputs
    ├── generate_dataset/       # Dataset generation code
    ├── result/                 # Experimental results directory, where experimental output results are stored
    │   ├── GraphInstruct/          # Output from the GraphInstruct dataset
    │   ├── GraphSCR/               # Output from the GraphSCR dataset
    │   └── GraphTRB/               # Output from the GraphTRB dataset
    ├── environments.yml        # Environment configuration file, used to set up the experiment environment
    ├── o1.txt                 # Project dependency documentation
    └── README.md              # Project description documentation

## How to use

- **Command line**:
    (Using qwen-7B model testing based on GraphInstruct dataset as an example)
    - Change directories:
        ```bash
        cd Code/GraphICL/evaluation/code_GraphInstruct/qwen-7B
        ```
    - Modify configuration parameters:
        ```json
        {
            "model_path": "/home/zch/Code/model/Qwen2.5-7B/Qwen/Qwen2___5-7B-Instruct",     // Model path
            "data_files": "/home/zch/Code/GraphICL/data/GraphInstruct.json",        // Dataset path
            "template": "query_template2",      // Using templates
            "template_icl": "query_template_icl2",      // Using templates
            "context_size": 16,     // Number of context examples
            "result_file": "test1"      // Identification of the test result file to be evaluated for accuracy
        }
        ```
    - Start the project:
        ```bash
        python IclAbilityTest.py            # generate the results for the no context case
        python IclAbilityTestResults.py     # Evaluate the accuracy of the results for the no context case
        python IcLExamples.py               # generate the results for the contextual use cases
        python IclExamplesTestResults.py    # Evaluate the accuracy of the results for the contextual use cases
        ```
    - Generate results:
        Results generated in the Code/GraphICL/result/GraphInstruct/qwen-7B, can modify the results generated directory path, result the folder as below:
        - responses: results for the no context case
        - task_accuracies: accuracy of the results for the no context case
        - responses_with_context_all_tasks: results for the contextual use cases
        - ICLtask_accuracies: accuracy of the results for the contextual use cases
    - Specific steps:
        1. Modify the configuration parameters and run the program file that generates the results for the no context case or the contextual use cases.
        2. Locate the results file under the results folder and determine the identification of the test result file.
        3. Modify the identification of the test result file to be evaluated for accuracy in the configuration parameter file, and run the program file that evaluate the accuracy of the results.
        4. Locate the accuracy of the results file in the result folder.

## Appendices

### Dataset GraphSCB

| same task | same graph | different question |
| --------- | ---------- | ----------------- |

Requirements:

Only `connectivity`, `shortest`, and `flow` questions will be extracted, as these questions can be changed
1. - According to the different number of nodes, it is divided into different difficulties
     `easy: [5,35]; middle: (35,65], hard: (65,100]`  
   - The number of graphs is as far as possible to extract 100, if there are not 100 graphs in the difficulty range, all of them are extracted
   
   - Create primary key `"graph"`, and key `"complexity"`
   
2. For each question, 16 questions of the same category were generated

3. Each question uses its own algorithm to calculate the correct answer to ensure that the answer is correct

4. The answer format uses `###` as a prefix
   eg:`### Yes` or `### No`

> [example]
>
> The `json` format of the dataset:
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

The corresponding file is `GraphSCB.json`

### Dataset GraphTRB

| different task | same graph | different question |
| -------------- | ---------- | ------------------ |

Requirements:

1. - 100 graphs, all extracted for `flow` class tasks
   - Create primary key `"graph"`
   - First we do the directed graph task, then we remove the pointing and do the undirected graph task.

2. - One for each of the seven different category questions was generated for each graph
   - Each immutable problem is augmented into nine problems, and a random edge deletion is not repeated. (Including the original one, deleted 8 times)
    We approximately treat the graph after removing an edge as the same as the original graph, so the value of '"graph"' does not change
   - Each modifiable question was expanded into 9 questions, and the question randomization was performed together with the data set. 
   
3. Each question uses its own algorithm to calculate the correct answer to ensure that the answer is correct

4. The answer format uses `###` as a prefix
   eg:`### Yes` or `### No`

> [example]
>
> The `json` format of the dataset:
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

The corresponding file is `GraphTRB.json`