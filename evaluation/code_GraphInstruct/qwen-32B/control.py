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
    file_path1 = "IclAbilityTest.py"  # 要运行的程序
    file_path2 = "IcLExamples.py"
    file_path3 = "IclAbilityTestResults.py"
    file_path4 = "IclExamplesTestResults.py"
    list1 = [
        ("query_template1", ["cycle"]), 
        ("query_template1", ["connectivity"]),
        ("query_template1", ["bipartite"]),
        ("query_template1", ["topology"]),
        ("query_template1", ["shortest"]),
        ("query_template1", ["triangle"]),
        ("query_template1", ["flow"]),
        ("query_template1", ["hamilton"]),
        ("query_template1", ["substructure"]),

        ("query_template2", ["cycle"]), 
        ("query_template2", ["connectivity"]),
        ("query_template2", ["bipartite"]),
        ("query_template2", ["topology"]),
        ("query_template2", ["shortest"]),
        ("query_template2", ["triangle"]),
        ("query_template2", ["flow"]),
        ("query_template2", ["hamilton"]),
        ("query_template2", ["substructure"])
    ]
    list2 = [
        ("query_template_icl1", 2, ["cycle"]),
        ("query_template_icl1", 2, ["connectivity"]),
        ("query_template_icl1", 2, ["bipartite"]),
        ("query_template_icl1", 2, ["topology"]),
        ("query_template_icl1", 2, ["shortest"]),
        ("query_template_icl1", 2, ["triangle"]),
        ("query_template_icl1", 2, ["flow"]),
        ("query_template_icl1", 2, ["hamilton"]),
        ("query_template_icl1", 2, ["substructure"]),

        ("query_template_icl2", 2, ["cycle"]),
        ("query_template_icl2", 2, ["connectivity"]),
        ("query_template_icl2", 2, ["bipartite"]),
        ("query_template_icl2", 2, ["topology"]),
        ("query_template_icl2", 2, ["shortest"]),
        ("query_template_icl2", 2, ["triangle"]),
        ("query_template_icl2", 2, ["flow"]),
        ("query_template_icl2", 2, ["hamilton"]),
        ("query_template_icl2", 2, ["substructure"]),

        ("query_template_icl1", 4, ["cycle"]),
        ("query_template_icl1", 4, ["connectivity"]),
        ("query_template_icl1", 4, ["bipartite"]),
        ("query_template_icl1", 4, ["topology"]),
        ("query_template_icl1", 4, ["shortest"]),
        ("query_template_icl1", 4, ["triangle"]),
        ("query_template_icl1", 4, ["flow"]),
        ("query_template_icl1", 4, ["hamilton"]),
        ("query_template_icl1", 4, ["substructure"]),

        ("query_template_icl2", 4, ["cycle"]),
        ("query_template_icl2", 4, ["connectivity"]),
        ("query_template_icl2", 4, ["bipartite"]),
        ("query_template_icl2", 4, ["topology"]),
        ("query_template_icl2", 4, ["shortest"]),
        ("query_template_icl2", 4, ["triangle"]),
        ("query_template_icl2", 4, ["flow"]),
        ("query_template_icl2", 4, ["hamilton"]),
        ("query_template_icl2", 4, ["substructure"]),

        ("query_template_icl1", 8, ["cycle"]),
        ("query_template_icl1", 8, ["connectivity"]),
        ("query_template_icl1", 8, ["bipartite"]),
        ("query_template_icl1", 8, ["topology"]),
        ("query_template_icl1", 8, ["shortest"]),
        ("query_template_icl1", 8, ["triangle"]),
        ("query_template_icl1", 8, ["flow"]),
        ("query_template_icl1", 8, ["hamilton"]),
        ("query_template_icl1", 8, ["substructure"]),

        ("query_template_icl2", 8, ["cycle"]),
        ("query_template_icl2", 8, ["connectivity"]),
        ("query_template_icl2", 8, ["bipartite"]),
        ("query_template_icl2", 8, ["topology"]),
        ("query_template_icl2", 8, ["shortest"]),
        ("query_template_icl2", 8, ["triangle"]),
        ("query_template_icl2", 8, ["flow"]),
        ("query_template_icl2", 8, ["hamilton"]),
        ("query_template_icl2", 8, ["substructure"])
    ]
    list3 = [
        "bipartite_query_template1_20250404_203933", 
        "connectivity_query_template1_20250404_110049", 
        "cycle_query_template1_20250404_101817", 
        "flow_query_template1_20250406_140444", 
        "hamilton_query_template1_20250406_190343", 
        "shortest_query_template1_20250406_034123", 
        "substructure_query_template1_20250407_085649", 
        "topology_query_template1_20250405_140338", 
        "triangle_query_template1_20250406_044946"
    ]
    list4 = [
        "2_query_template_icl1_20250329_065735", "2_query_template_icl2_20250329_075645",
        "4_query_template_icl1_20250329_084928", "4_query_template_icl2_20250329_094853",
        "8_query_template_icl1_20250329_104757", "8_query_template_icl2_20250329_114242"
    ]

    # for value, task in list1:
    #     # 使用函数来更新
    #     update(json_file_path, "template", value)
    #     update(json_file_path, "task_types", task)
    #     # 启动Python程序
    #     p = subprocess.Popen(["python", file_path1])
    #     p.wait()

    # for value1, value2, task in list2:
    #     # 使用函数来更新
    #     update(json_file_path, "template_icl", value1)
    #     update(json_file_path, "context_size", value2)
    #     update(json_file_path, "task_types", task)
    #     # 启动Python程序
    #     p = subprocess.Popen(["python", file_path2])
    #     p.wait()

    for value in list3:
        # 使用函数来更新
        update(json_file_path, "result_file", value)
        # 启动Python程序
        p = subprocess.Popen(["python", file_path3])
        p.wait()

    # for value in list4:
    #     # 使用函数来更新
    #     update(json_file_path, "result_file", value)
    #     # 启动Python程序
    #     p = subprocess.Popen(["python", file_path4])
    #     p.wait()

if __name__ == '__main__':
    main()