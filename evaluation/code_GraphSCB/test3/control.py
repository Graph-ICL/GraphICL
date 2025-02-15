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
        ("query_template_icl1", "group1"), ("query_template_icl2", "group1"),
        ("query_template_icl1", "group2"), ("query_template_icl2", "group2")
    ]
    list2 = [
        "group1_query_template_icl1_20250204_232234", "group1_query_template_icl2_20250205_032557",
        "group2_query_template_icl1_20250205_034133", "group2_query_template_icl2_20250205_075738"
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