import subprocess
import json


def update(json_file_path, type, new):
    # 读取JSON文件内容
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)  # 加载JSON数据到Python字典中
    # 修改的值
    data[type] = new
    # 将更新后的数据写回到JSON文件中
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def main():
    json_file_path = 'config.json'  # 配置文件
    file_path1 = "IcLExamples.py"   # 要运行的程序
    file_path2 = "IclExamplesTestResults.py"
    list1 = [
        ("query_template_icl1", "cycle"), ("query_template_icl2", "cycle"),
        ("query_template_icl1", "connectivity"), ("query_template_icl2", "connectivity"),
        ("query_template_icl1", "bipartite"), ("query_template_icl2", "bipartite"),
        ("query_template_icl1", "topology"), ("query_template_icl2", "topology"),
        ("query_template_icl1", "shortest"), ("query_template_icl2", "shortest"),
        ("query_template_icl1", "flow"), ("query_template_icl2", "flow"),
        ("query_template_icl1", "hamilton"), ("query_template_icl2", "hamilton")
    ]
    list2 = [
        "bipartite_query_template_icl1_20250206_010939", "bipartite_query_template_icl2_20250206_045032",
        "connectivity_query_template_icl1_20250207_075841", "connectivity_query_template_icl2_20250207_104028",
        "cycle_query_template_icl1_20250205_125139", "cycle_query_template_icl2_20250206_004837",
        "flow_query_template_icl1_20250206_183721", "flow_query_template_icl2_20250206_223028",
        "hamilton_query_template_icl1_20250206_224717", "hamilton_query_template_icl2_20250207_055445",
        "shortest_query_template_icl1_20250206_114212", "shortest_query_template_icl2_20250206_181921",
        "topology_query_template_icl1_20250206_051044", "topology_query_template_icl2_20250206_112415"
    ]


    # for value1, value2 in list1:
    #     # 使用函数来更新
    #     update(json_file_path, "template_icl", value1)
    #     update(json_file_path, "question", value2)
    #     # 启动Python程序
    #     p = subprocess.Popen(["python", file_path1])
    #     p.wait()

    for value in list2:
        # 使用函数来更新
        update(json_file_path, "result_file", value)
        # 启动Python程序
        p = subprocess.Popen(["python", file_path2])
        p.wait()

if __name__ == '__main__':
    main()