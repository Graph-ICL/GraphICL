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
        "query_template1", "query_template2"
    ]
    list2 = [
        ("query_template_icl1", 2), ("query_template_icl2", 2),
        ("query_template_icl1", 4), ("query_template_icl2", 4),
        ("query_template_icl1", 8), ("query_template_icl2", 8),
        ("query_template_icl1", 16), ("query_template_icl2", 16)
    ]
    list3 = [
        "query_template1_20250129_104205", "query_template2_20250129_124704"
    ]
    list4 = [
        "2_query_template_icl1_20250129_132249", "2_query_template_icl2_20250129_164237",
        "4_query_template_icl1_20250129_174705", "4_query_template_icl2_20250129_214423",
        "8_query_template_icl1_20250129_234800", "8_query_template_icl2_20250130_045100",
        "16_query_template_icl1_20250211_140603", "16_query_template_icl2_20250212_012338"
    ]

    for value in list1:
        # 使用函数来更新
        update(json_file_path, "template", value)
        # 启动Python程序
        p = subprocess.Popen(["python", file_path1])
        p.wait()

    for value1, value2 in list2:
        # 使用函数来更新
        update(json_file_path, "template_icl", value1)
        update(json_file_path, "context_size", value2)
        # 启动Python程序
        p = subprocess.Popen(["python", file_path2])
        p.wait()

    for value in list3:
        # 使用函数来更新
        update(json_file_path, "result_file", value)
        # 启动Python程序
        p = subprocess.Popen(["python", file_path3])
        p.wait()

    for value in list4:
        # 使用函数来更新
        update(json_file_path, "result_file", value)
        # 启动Python程序
        p = subprocess.Popen(["python", file_path4])
        p.wait()

if __name__ == '__main__':
    main()