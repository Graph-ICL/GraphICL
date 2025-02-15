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
        ("query_template_icl1", "easy", 2), ("query_template_icl2", "easy", 2),
        ("query_template_icl1", "middle", 2), ("query_template_icl2", "middle", 2),
        ("query_template_icl1", "hard", 2), ("query_template_icl2", "hard", 2),
        ("query_template_icl1", "easy", 4), ("query_template_icl2", "easy", 4),
        ("query_template_icl1", "middle", 4), ("query_template_icl2", "middle", 4),
        ("query_template_icl1", "hard", 4), ("query_template_icl2", "hard", 4),
        ("query_template_icl1", "easy", 8), ("query_template_icl2", "easy", 8),
        ("query_template_icl1", "middle", 8), ("query_template_icl2", "middle", 8),
        ("query_template_icl1", "hard", 8), ("query_template_icl2", "hard", 8)
    ]
    list2 = [
        "2_easy_query_template_icl1_20250205_065455", "2_easy_query_template_icl2_20250205_145948",
        "2_hard_query_template_icl1_20250206_071312", "2_hard_query_template_icl2_20250206_170500",
        "2_middle_query_template_icl1_20250205_201029", "2_middle_query_template_icl2_20250206_063843",
        "4_easy_query_template_icl1_20250206_173347", "4_easy_query_template_icl2_20250207_014258",
        "4_hard_query_template_icl1_20250207_134235", "4_hard_query_template_icl2_20250208_231608",
        "4_middle_query_template_icl1_20250207_023416", "4_middle_query_template_icl2_20250207_122946",
        "8_easy_query_template_icl1_20250208_235934", "8_easy_query_template_icl2_20250209_095026",
        "8_hard_query_template_icl1_20250210_020737", "8_hard_query_template_icl2_20250210_160846",
        "8_middle_query_template_icl1_20250209_113100", "8_middle_query_template_icl2_20250209_234210"
    ]


    # for value1, value2, value3 in list1:
    #     # 使用函数来更新
    #     update(json_file_path, "template_icl", value1)
    #     update(json_file_path, "example_difficulty", value2)
    #     update(json_file_path, "context_size", value3)
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